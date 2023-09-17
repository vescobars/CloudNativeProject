""" Pydantic schemas for request and response bodies """
import uuid
from datetime import datetime

from pydantic import BaseModel, UUID4

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


class PostWithRouteSchema(BaseModel):
    """The inner class returned in data by RF003"""
    id: UUID4
    userId: UUID4
    createdAt: datetime
    expireAt: datetime
    route: CreatedRouteSchema


class CreatePostResponseSchema(BaseModel):
    """
        Sent after creating an offer successfully
        """
    data: PostWithRouteSchema
    msg: str
