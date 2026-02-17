# schemas/output_parser.py

import json
from pydantic import ValidationError
from schemas.itinerary import Itinerary
from utils.logger import setup_logger

logger = setup_logger()


class PydanticOutputParser:
    def parse(self, text: str) -> Itinerary:
        logger.info("Parsing output...")
        try:
            # logger.debug(f"Raw output to parse: {text}") # Optional: log raw text if needed
            json_data = json.loads(text)
            return Itinerary.model_validate(json_data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError(f"Invalid JSON output from model: {e}")
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise ValueError(f"Schema validation failed: {e}")
