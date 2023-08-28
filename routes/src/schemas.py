"""Pydantic schema for Routes"""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, UUID4, Field
from src.constants import now_utc


class RouteSchema(BaseModel):
    """
    Defines the pydantic schema for a given Route
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(default_factory=uuid.uuid4)
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime = now_utc()
    updateAt: datetime = now_utc()
