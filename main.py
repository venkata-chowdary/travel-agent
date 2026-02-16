# main.py

import os
from dotenv import load_dotenv
from agent.agent import GeminiAgent
from schemas.itinerary import Itinerary
from config import MODEL_NAME

load_dotenv()

agent = GeminiAgent(api_key=os.getenv("GEMINI_API_KEY"))

user_query = "Plan a 3-day trip to Goa from Delhi under ₹20,000 next weekend."

raw_response = agent.run(user_query)
print("Raw Response from Gemini:")
print(raw_response)