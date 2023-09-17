""" Pydantic schemas for request and response bodies """
from datetime import datetime
from typing import List

from pydantic import BaseModel, UUID4

from src.schemas import BagSize, Location


class ImprovedRouteSchema(BaseModel):
    """More hierarchical schema for a Route"""
    id: UUID4
    flightId: str
    origin: Location
    destiny: Location
    bagCost: int


class ScoredOfferSchema(BaseModel):
    """OfferSchema that also includes utility score"""
    id: UUID4
    userId: UUID4
    description: str
    size: BagSize
    fragile: bool
    offer: float
    score: float
    createdAt: datetime


class RF005ResponseSchema(BaseModel):
    """The full response of RF005, a post's info, including its route and sorted list of offers"""
    id: UUID4

    route: ImprovedRouteSchema

    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime
    expireAt: datetime
    offers: List[ScoredOfferSchema]


class WrappedRF005ResponseSchema(BaseModel):
    """A wrapped version of the RF005 response, to fit specification"""
    data: RF005ResponseSchema
