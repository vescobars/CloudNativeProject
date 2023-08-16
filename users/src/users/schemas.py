""" Pydantic schemas for request and response bodiess """
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


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
