from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UserQuery(BaseModel):
    model_config = ConfigDict(extra='ignore')

    origin: str = Field(..., description="Origin city", min_length=2)
    destination: str =Field(..., description="Destination city", min_length=2)
    days: int = Field(..., description="Number of days", ge=0, le=14)
    budget: float = Field(..., description="Budget", ge=0)
    travel_date: Optional[str] = None
