from pydantic import BaseModel

class Itinerary(BaseModel):
    destination: str
    total_cost: float
    flight_details: dict
    hotel_details: dict
    weather_details:str
    notes:str
    
    