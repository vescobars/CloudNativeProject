""" Pydantic schemas for request and response bodiess """
import uuid
from pydantic import BaseModel, Field


class CreateUtilityRequestSchema(BaseModel):
    """
    Used when creating a utility
    """
    offer_id: uuid.UUID = Field(min_length=1)
    utility: float


def check_uuid4(v: str) -> str:
    """Returns value error if str is not a valid UUID4"""
    uuid.UUID(v)
    return v


class UpdateUtilityRequestSchema(BaseModel):
    """
    Used when updating a utility
    """
    utility: float
