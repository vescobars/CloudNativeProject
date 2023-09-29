""" Pydantic schemas for request and response bodies """
from datetime import datetime

from pydantic import BaseModel, UUID4, Field

from src.schemas import IssuerEnum, StatusEnum


class CreateCCRequestSchema(BaseModel):
    """
    Used when creating a Credit Card
    """
    cardNumber: str = Field(regex=r'\d{16}')
    cvv: str = Field(regex=r'\d{3,4}')
    expirationDate: str = Field(regex=r'\d{2}/\d{2}')
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


class UpdateCCStatusRequestSchema(BaseModel):
    """
    Used when updating a Credit Card status
    """
    createdAt: datetime
    transactionIdentifier: str
    status: StatusEnum
