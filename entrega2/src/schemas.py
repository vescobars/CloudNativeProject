""" Pydantic models for all global entities """
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, UUID4, Field


class BagSize(Enum):
    LARGE = 'LARGE'
    MEDIUM = 'MEDIUM'
    SMALL = 'SMALL'


class OfferSchema(BaseModel):
    """Schema used to represent an offer"""
    id: UUID4
    userId: UUID4
    description: str
    size: BagSize
    fragile: bool
    offer: float
    createdAt: datetime
    postId: UUID4


class CreatedOfferSchema(BaseModel):
    """Schema used to represent a recently created offer"""
    id: UUID4
    userId: UUID4
    createdAt: datetime
    postId: UUID4


class CreatedPostSchema(BaseModel):
    """Schema used to represent a recently created post"""
    id: UUID4
    userId: UUID4
    createdAt: datetime
    routeId: UUID4


class UtilitySchema(BaseModel):
    """
    Defines the pydantic model (schema) for Utility
    """
    model_config = ConfigDict(from_attributes=True)

    offer_id: UUID4
    utility: float

    createdAt: datetime = Field(default_factory=datetime.now)
    updateAt: datetime = Field(default_factory=datetime.now)


class PostSchema(BaseModel):
    """
    Defined pydantic model for a Post
    """
    id: UUID4
    routeId: UUID4
    userId: UUID4
    expireAt: datetime
    createdAt: datetime


class RouteSchema(BaseModel):
    """
    Defined pydantic model for a Route
    """
    id: UUID4
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime
