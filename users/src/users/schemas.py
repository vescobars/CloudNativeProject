""" Pydantic schemas for request and response bodiess """
import uuid
from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, Field, AfterValidator

from src.schemas import UserStatusEnum


class CreateUserRequestSchema(BaseModel):
    """
    Used when creating a user
    """
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    email: EmailStr = Field(min_length=1)
    phoneNumber: Optional[str] = None
    dni: Optional[str] = None
    fullName: Optional[str] = None


def check_uuid4(v: str) -> str:
    """Returns value error if str is not a valid UUID4"""
    uuid.UUID(v)
    return v


class CreateUserResponseSchema(BaseModel):
    """
    Returned when creating a user successfully
    """
    id: str = Annotated[str, AfterValidator(check_uuid4)]
    createdAt: str


class UpdateUserRequestSchema(BaseModel):
    """
    Used when updating a user
    """
    status: Optional[UserStatusEnum] = None
    phoneNumber: Optional[str] = None
    dni: Optional[str] = None
    fullName: Optional[str] = None
