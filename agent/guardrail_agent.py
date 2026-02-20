from google import genai
from utils.logger import setup_logger
from agent.prompts import GUARDRAIL_PROMPT
from config import MODEL_NAME,TEMPERATURE
import json

logger = setup_logger()

class GuardrailAgent:
    def __init__(self, api_key: str, output_parser: None):
        self.client=genai.Client(api_key=api_key)
        self.output_parser=output_parser

    def run(self, user_query:str):
        logger.info("Initializing Guardrail Agent...")
        messages = [
            {"role": "system", "parts": [{"text":GUARDRAIL_PROMPT}]},
            {"role": "user", "parts": [{"text":user_query}]}
        ]

        response=self.client.models.generate_content(
        model=MODEL_NAME, 
        contents=messages, 
        config={
        "temperature": TEMPERATURE
        })
        logger.info(f"Model {MODEL_NAME} succeeded.")
    
        return self.parse_and_validate(response.text)

    def parse_and_validate(self, response_text: str) -> bool:
        """Parses the guardrail JSON response and validates the query."""
        
        # Clean up markdown if present
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()

        try:
            guardrail_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse guardrail response: {e}")
            raise ValueError("Invalid JSON format in guardrail response.")

        if not guardrail_data.get("isRequestValid"):
            reason = guardrail_data.get("reason", "Irrelevant query.")
            logger.warning(f"Invalid query: {reason}")
            raise ValueError(f"Guardrail blocked query: {reason}")
            
        return True
    