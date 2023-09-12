""" Pydantic models for all global entities """
from datetime import datetime

from pydantic import BaseModel, ConfigDict, UUID4, Field


class OfferSchema(BaseModel):
    """Schema used to represent an offer"""
    id: UUID4
    userId: str
    createdAt: datetime
    postId: str


class UtilitySchema(BaseModel):
    """
    Defines the pydantic model (schema) for Utility
    """
    model_config = ConfigDict(from_attributes=True)

    offer_id: UUID4
    utility: float

    createdAt: datetime = Field(default_factory=datetime.now)
    updateAt: datetime = Field(default_factory=datetime.now)
