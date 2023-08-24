""" Pydantic schemas for req and response bodies"""

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
class CreateRouteRequestSchema(BaseModel):
    """
    Request schema used when creating a new route
    """
    flightId: str = Field(min_length=1)
    sourceAirportCode: str = Field(min_length=1)
    sourceCountry: str = Field(min_length=1)
    destinyAirportCode: Field(min_length=1)
    destinyCountry: str = Field(min_length=1)
    bagCost: int = Field(ge=0)
    plannedStartDate: datetime = Field()
    plannedEndDate: datetime = Field()
