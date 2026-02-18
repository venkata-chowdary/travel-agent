from exceptiongroup import catch
from google import genai
from config import MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS
from agent.prompts import SYSTEM_PROMPT
from schemas.tool_schema import SEARCH_FLIGHTS_SCHEMA
from schemas.tool_schema import SEARCH_FLIGHTS_SCHEMA
from tools.flights import search_flights
from utils.logger import setup_logger
from config import FALLBACK_GEMINI_MODELS
logger = setup_logger()


class GeminiAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

        self.tools = {
            "search_flights": search_flights
        }

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
        
        for i in range(5):
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
                        "tools": [{"function_declarations": [SEARCH_FLIGHTS_SCHEMA]}]
                    })
                    logger.info(f"Model {MODEL} succeeded.")
                    break
                
                except Exception as e:
                    error=e
                    if e.code==429:
                        logger.warning(f"Rate limit hit for {MODEL}, trying fallback...")
                        continue
                    else:
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
                logger.info("Final answer received.")
                return response.text

        raise RuntimeError("Max tool iterations exceeded")
