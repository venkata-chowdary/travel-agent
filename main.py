# main.py

import os
import json
import asyncio
from dotenv import load_dotenv
from agent.agent import GeminiAgent
from agent.guardrail_agent import GuardrailAgent
from schemas.output_parser import PydanticOutputParser
from utils.logger import setup_logger

load_dotenv()

logger = setup_logger()
parser = PydanticOutputParser()


async def main():
    logger.info("Initializing Gemini Agent...")

    agent = GeminiAgent(
        api_key=os.getenv("GEMINI_API_KEY"),
        output_parser=parser
    )

    guardrail_agent = GuardrailAgent(
        api_key=os.getenv("GEMINI_API_KEY"),
        output_parser=parser
    )

    logger.info("Starting Travel Agent Application")

    user_query = "Plan a 3-day trip to Goa from Delhi under ₹20,000 next weekend."
    logger.info(f"User Query: {user_query}")

    try:
        # Guardrail agent now raises ValueError if invalid
        guardrail_agent.run(user_query)
        logger.info("Query is valid. Proceeding to planner agent.")

        raw_response = agent.run(user_query)

    except Exception as e:
        logger.error(f"Agent failed to generate response: {e}")
        raise

    logger.info("Parsing response...")
    itinerary = parser.parse(raw_response)

    logger.info("Response parsed successfully.")
    print("\n✅ FINAL ITINERARY (Validated)\n")
    print(itinerary.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
