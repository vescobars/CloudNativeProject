""" Pydantic schemas for request and response bodies """
import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateRoutePostRequestSchema(BaseModel):
    """
    Used when creating an Offer
    """
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime
    expireAt: datetime


class CreatedRouteSchema(BaseModel):
    """
    Response returned by POST /offer
    """
    id: uuid.UUID
    createdAt: datetime
