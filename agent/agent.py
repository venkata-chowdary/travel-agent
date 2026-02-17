from google import genai
from config import MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS
from agent.prompts import SYSTEM_PROMPT
from schemas.tool_schema import SEARCH_FLIGHTS_SCHEMA
from schemas.tool_schema import SEARCH_FLIGHTS_SCHEMA
from tools.flights import search_flights
from utils.logger import setup_logger

logger = setup_logger()


class GeminiAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

        # tool registry (expand later)
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

        for i in range(5):  # 🔒 max iterations
            logger.info(f"Iteration {i+1}...")
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config={
                    "temperature": TEMPERATURE,
                    "max_output_tokens": MAX_OUTPUT_TOKENS,
                    "tools": [{"function_declarations": [SEARCH_FLIGHTS_SCHEMA]}]
                }
            )

            candidate = response.candidates[0]
            part = candidate.content.parts[0]

            # 🔧 Tool call detected
            if hasattr(part, "function_call") and part.function_call:
                tool_name = part.function_call.name
                tool_args = dict(part.function_call.args)
                
                logger.info(f"Tool call detected: {tool_name} with args: {tool_args}")

                if tool_name not in self.tools:
                    raise ValueError(f"Unknown tool: {tool_name}")

                # Execute tool
                try:
                    tool_result = self.tools[tool_name](**tool_args)
                    logger.info(f"Tool result: {tool_result}")
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}")
                    raise

                # Send tool result back to model
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
                # ✅ Final answer (no more tool calls)
                logger.info("Final answer received.")
                return response.text

        raise RuntimeError("Max tool iterations exceeded")
