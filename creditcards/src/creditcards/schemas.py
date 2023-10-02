""" Pydantic schemas for request and response bodies """
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, UUID4, Field, field_validator

from src.schemas import IssuerEnum, StatusEnum


class CreateCCRequestSchema(BaseModel):
    """
    Used when creating a Credit Card
    """
    cardNumber: str = Field(pattern=r'\d{16}')
    cvv: str = Field(pattern=r'\d{3,4}')
    expirationDate: str = Field(pattern=r'\d{2}/\d{2}')
    cardHolderName: str


class CreateCCResponseSchema(BaseModel):
    """
        Sent after creating a credit card successfully
        """
    id: UUID4
    userId: UUID4
    createdAt: str


class TrueNativeRegisterCardResponseSchema(BaseModel):
    """
    Object returned after registering card in Truenative successfully
    """
    RUV: str
    token: str
    issuer: IssuerEnum
    transactionIdentifier: str
    createdAt: datetime

    @field_validator('createdAt', mode="before")
    @classmethod
    def parse_string_datetime(cls, dt) -> datetime:
        if type(dt) is datetime:
            return dt
        # Parses a string of the format 'Sat, 30 Sep 2023 22:57:26 GMT' to a datetime object
        return datetime.strptime(dt, '%a, %d %b %Y %H:%M:%S %Z')


class UpdateCCStatusRequestSchema(BaseModel):
    """
    Used when updating a Credit Card status
    """
    createdAt: Optional[str]
    transactionIdentifier: str
    status: StatusEnum
