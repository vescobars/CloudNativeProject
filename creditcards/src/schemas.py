""" Pydantic models for all global entities """
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, UUID4, Field


class IssuerEnum(Enum):
    """
    The card issuer
    """
    VISA = 'VISA'
    MASTERCARD = 'MASTERCARD'
    AMERICAN_EXPRESS = 'AMERICAN_EXPRESS'
    DISCOVER = 'DISCOVER'
    OTHER = 'OTHER'
    UNKNOWN = 'UNKNOWN'


class StatusEnum(Enum):
    """
    The card status
    """
    POR_VERIFICAR = 'POR_VERIFICAR'
    RECHAZADA = 'RECHAZADA'
    APROBADA = 'APROBADA'


class CreditCardSchema(BaseModel):
    """
    Defines the pydantic model (schema) for CreditCard
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    token: str = Field(max_length=256, min_length=256)
    userId: UUID4
    lastFourDigits: str
    ruv: str
    issuer: IssuerEnum
    status: StatusEnum

    createdAt: datetime = Field(default_factory=datetime.now)
    updateAt: datetime = Field(default_factory=datetime.now)


class CreditCardListItemSchema(BaseModel):
    """
    Defines the pydantic model (schema) for a CreditCard belonging to a list
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    token: str
    userId: UUID4
    lastFourDigits: str
    issuer: IssuerEnum
    status: StatusEnum

    createdAt: datetime = Field()
    updateAt: datetime = Field()
