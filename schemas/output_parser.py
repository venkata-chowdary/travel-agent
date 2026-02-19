# schemas/output_parser.py

import json
import re
from pydantic import ValidationError
from schemas.itinerary import Itinerary
from utils.logger import setup_logger

logger = setup_logger()


class PydanticOutputParser:
    def parse(self, text: str) -> Itinerary:
        logger.info("Parsing output...")
        try:
            # Try to find JSON block using regex
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
            if match:
                json_str = match.group(1)
            else:
                # If no code block, try to find the first '{' and last '}'
                try:
                    start_idx = text.index('{')
                    end_idx = text.rindex('}') + 1
                    json_str = text[start_idx:end_idx]
                except ValueError:
                    # If no braces found, assume the whole text might be JSON (or it's invalid)
                    json_str = text

            json_str = json_str.strip()
            
            logger.debug(f"Raw output to parse: {json_str}") 
            json_data = json.loads(json_str)
            return Itinerary.model_validate(json_data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.error(f"Failed text content: {text}")
            raise ValueError(f"Invalid JSON output from model: {e}")
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise ValueError(f"Schema validation failed: {e}")
