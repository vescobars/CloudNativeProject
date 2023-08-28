""" Pydantic schemas for request and response bodiess """
import datetime
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


class GenerateTokenRequestSchema(BaseModel):
    """
    Used when requesting a new token
    """
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class GenerateTokenResponseSchema(BaseModel):
    """
    Used when requesting a new token
    """
    id: uuid.UUID
    token: str
    expireAt: datetime.datetime


class GetUserResponseSchema(BaseModel):
    """
    Used when requesting a user
    """
    id: uuid.UUID
    username: str
    email: str
    fullName: Optional[str] = ""
    dni: Optional[str] = ""
    phoneNumber: Optional[str] = ""
    status: str
