from pydantic import Field, BaseModel

class TripRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=500)
