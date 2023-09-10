""" Pydantic schemas for request and response bodiess """
import uuid
from enum import Enum
from pydantic import BaseModel, Field


class BagSize(Enum):
    LARGE = 'LARGE'
    MEDIUM = 'MEDIUM'
    SMALL = 'SMALL'


class CreateUtilityRequestSchema(BaseModel):
    """
    Used when creating a utility
    """
    offer_id: uuid.UUID = Field(min_length=1)
    offer: float
    size: BagSize
    bag_cost: int


def check_uuid4(v: str) -> str:
    """Returns value error if str is not a valid UUID4"""
    uuid.UUID(v)
    return v


class UpdateUtilityRequestSchema(BaseModel):
    """
    Used when updating a utility
    """
    offer: float
    size: BagSize
    bag_cost: int
