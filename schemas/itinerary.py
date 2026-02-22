from pydantic import BaseModel, Field, ConfigDict
from typing import Dict

class Itinerary(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    destination: str = Field(..., description="Destination for the trip")
    total_cost: float = Field(..., ge=0,description="Total cost of the trip")
    flight_details: Dict = Field(..., description="Details of the flight")
    hotel_details: Dict =Field(..., description="Details of the hotel")
    weather_details:str = Field(..., description="Weather details")
    notes:str = Field(..., description="Notes or extra details")    