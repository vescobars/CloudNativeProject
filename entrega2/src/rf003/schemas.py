""" Pydantic schemas for request and response bodies """
import uuid
from datetime import datetime

from pydantic import BaseModel

from src.schemas import Location


class CreateRoutePostRequestSchema(BaseModel):
    """
    Used when creating a Route
    """
    flightId: str
    expireAt: datetime
    plannedStartDate: datetime
    plannedEndDate: datetime

    origin: Location
    destiny: Location

    bagCost: int


class CreatedRouteSchema(BaseModel):
    """
    Response returned by POST /offer
    """
    id: uuid.UUID
    createdAt: datetime
