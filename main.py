# main.py

import os
from dotenv import load_dotenv
from agent.agent import GeminiAgent
from schemas.output_parser import PydanticOutputParser
from utils.logger import setup_logger

load_dotenv()

logger = setup_logger()
agent = GeminiAgent(api_key=os.getenv("GEMINI_API_KEY"))
parser = PydanticOutputParser()

logger.info("Starting Travel Agent Application")
user_query = "Plan a 3-day trip to Goa from Delhi under ₹20,000 next weekend."

logger.info(f"User Query: {user_query}")
raw_response = agent.run(user_query)

logger.info("Parsing response...")
itinerary = parser.parse(raw_response)

logger.info("Response parsed successfully.")
print("\n✅ FINAL ITINERARY (Validated)\n")
print(itinerary.model_dump_json(indent=2))
