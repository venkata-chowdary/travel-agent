from fastapi import APIRouter, HTTPException
from schema import TripRequest
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import GeminiAgent
from agent.guardrail_agent import GuardrailAgent
from schemas.output_parser import PydanticOutputParser

load_dotenv()

router=APIRouter()

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
        # 1. Validate query using guardrail agent
        guardrail_agent.run(request.query)
        
        # 2. Generate trip plan using the main agent
        raw_response = agent.run(request.query)
        
        # 3. Parse the output into a Pydantic model
        itinerary = parser.parse(raw_response)
        
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