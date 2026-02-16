from google import genai
from config import MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS
from agent.prompts import SYSTEM_PROMPT


class GeminiAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def run(self, user_message: str) -> str:
        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                {
                    "role": "system",
                    "parts": [{"text": SYSTEM_PROMPT}]
                },
                {
                    "role": "user",
                    "parts": [{"text": user_message}]
                }
            ],
            config={
                "temperature": TEMPERATURE,
                # "max_output_tokens": MAX_OUTPUT_TOKENS
            }
        )

        return response.text
