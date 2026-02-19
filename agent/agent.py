from exceptiongroup import catch
import time
from google import genai
from config import MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS
from agent.prompts import SYSTEM_PROMPT
from schemas.tool_schema import SEARCH_FLIGHTS_SCHEMA, SEARCH_HOTELS_SCHEMA,CALCULATE_TOTAL_COST_SCHEMA
from tools.flights import search_flights
from utils.logger import setup_logger
from config import FALLBACK_GEMINI_MODELS
from agent.tool import TOOL_REGISTRY
logger = setup_logger()


class GeminiAgent:

    def __init__(self, api_key: str, output_parser=None):
        self.client = genai.Client(api_key=api_key)
        self.tools = TOOL_REGISTRY
        self.output_parser = output_parser
        
    def run(self, user_message: str):
        logger.info(f"Agent received message: {user_message}")
        messages = [
            {
                "role": "system",
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            {
                "role": "user",
                "parts": [{"text": user_message}]
            }
        ]
        
        # Increased iteration limit to allow for retries
        for i in range(10):
            logger.info(f"Iteration {i+1}...")
            response=None
            
            for MODEL in FALLBACK_GEMINI_MODELS:
                try:
                    logger.info(f"Trying model: {MODEL}")
                    response = self.client.models.generate_content(
                    model=MODEL,
                    contents=messages,
                    config={
                        "temperature": TEMPERATURE,
                        "max_output_tokens": MAX_OUTPUT_TOKENS,
                        "tools": [{"function_declarations": [SEARCH_FLIGHTS_SCHEMA, SEARCH_HOTELS_SCHEMA, CALCULATE_TOTAL_COST_SCHEMA]}]
                    })
                    logger.info(f"Model {MODEL} succeeded.")
                    break
                
                except Exception as e:
                    logger.error(f"Model {MODEL} failed with error: {repr(e)}")
                    status_code = getattr(e, "code", None)

                    if status_code == 429:
                        import re
                        match = re.search(r"retry in (\d+(\.\d+)?)s", str(e))
                        if match:
                            wait_time = float(match.group(1)) + 1  # Add 1 second buffer
                        else:
                            wait_time = 5 * (2 ** i) # Fallback exponential backoff
                            
                        logger.warning(f"Rate limit hit for {MODEL}. Waiting for {wait_time:.2f} seconds before trying fallback...")
                        time.sleep(wait_time) 
                        continue

                    if e.__class__.__name__ in ("ConnectError", "TimeoutError"):
                        logger.warning(f"Network error with {MODEL}, trying fallback...")
                        time.sleep(1) 
                        continue    
                    raise

            if response is None:
                raise RuntimeError(f"All models exhausted.")
            
            candidate = response.candidates[0]
            part = candidate.content.parts[0]

            if hasattr(part, "function_call") and part.function_call:
                tool_name = part.function_call.name
                tool_args = dict(part.function_call.args)
                
                logger.info(f"Tool call detected: {tool_name} with args: {tool_args}")

                if tool_name not in self.tools:
                    raise ValueError(f"Unknown tool: {tool_name}")

                try:
                    tool_result = self.tools[tool_name](**tool_args)
                    logger.info(f"Tool result: {tool_result}")
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}")
                    raise

                messages.append({
                    "role": "tool",
                    "parts": [{
                        "function_response": {
                            "name": tool_name,
                            "response": {"content": tool_result}
                        }
                    }]
                })

            else:
                logger.info("Final answer received. Validating...")
                response_text = response.text
                
                if self.output_parser:
                    try:
                        self.output_parser.parse(response_text)
                        logger.info("Validation successful.")
                        return response_text
                    except ValueError as e:
                        logger.warning(f"Validation failed: {e}. Retrying...")
                        messages.append({
                            "role": "model",
                            "parts": [{"text": response_text}]
                        })
                        messages.append({
                            "role": "user",
                            "parts": [{"text": f"Error parsing JSON: {e}. Please correct the JSON output."}]
                        })
                        continue
                
                return response_text

        raise RuntimeError("Max tool iterations exceeded")
