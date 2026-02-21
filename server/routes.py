from fastapi import APIRouter, HTTPException
from schema import TripRequest
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import GeminiAgent
from agent.guardrail_agent import GuardrailAgent
from schemas.output_parser import PydanticOutputParser
from redis.asyncio import Redis
import json
from helper import generate_itinerary_hash

load_dotenv()

router=APIRouter()

redis_client = Redis(host='localhost', port=6379, db=0)

parser = PydanticOutputParser()

# Initialize agents
agent = GeminiAgent(
    api_key=os.getenv("GEMINI_API_KEY"),
    output_parser=parser
)

guardrail_agent = GuardrailAgent(
    api_key=os.getenv("GEMINI_API_KEY"),
    output_parser=parser
)

@router.post("/plan-trip", status_code=200)
async def plan_trip(request: TripRequest):
    try:
        itinerary_obj = guardrail_agent.run(request.query)
        
        itinerary_hash = generate_itinerary_hash(itinerary_obj)

        print("checking cache for hash:", itinerary_hash)
        cached_plan = await redis_client.get(itinerary_hash)
        if cached_plan:
            print("using cached plan:", cached_plan)
            return {
                "message": "Trip planned successfully (cached)",
                "itinerary": json.loads(cached_plan)
            }
        
        raw_response = agent.run(request.query)
        itinerary = parser.parse(raw_response)
        
        await redis_client.set(itinerary_hash, json.dumps(itinerary.model_dump()), ex=86400)
        
        return {
            "message": "Trip planned successfully",
            "itinerary": itinerary.model_dump()
        }
    except ValueError as ve:
        # Guardrail rejection or parsing error
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # General exceptions
        raise HTTPException(status_code=500, detail=str(e))