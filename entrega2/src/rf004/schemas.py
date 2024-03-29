""" Pydantic schemas for request and response bodies """
import datetime
import uuid

from pydantic import BaseModel

from src.schemas import CreatedOfferSchema, BagSize


class CreateOfferRequestSchema(BaseModel):
    """
    Used when creating an Offer
    """
    description: str
    size: BagSize
    fragile: bool
    offer: float


def check_uuid4(v: str) -> str:
    """Returns value error if str is not a valid UUID4"""
    uuid.UUID(v)
    return v


class CreateOfferResponseSchema(BaseModel):
    """
    Sent after creating an offer successfully
    """
    data: CreatedOfferSchema
    msg: str


class PostOfferResponseSchema(BaseModel):
    """
    Response returned by POST /offer
    """
    id: uuid.UUID
    userId: uuid.UUID
    createdAt: datetime.datetime


class CreateUtilityRequestSchema(BaseModel):
    """
    Used when creating a utility
    """
    offer_id: uuid.UUID
    offer: float
    size: BagSize
    bag_cost: int


class UpdateUtilityRequestSchema(BaseModel):
    """
    Used when updating a utility
    """
    offer: float
    size: BagSize
    bag_cost: int
