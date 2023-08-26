""" Pydantic models for all global entities """
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4, Field, EmailStr


class UserStatusEnum(str, Enum):
    """
    Defines the available statuses for a user
    """
    POR_VERIFICAR = 'POR_VERIFICAR'
    NO_VERIFICADO = 'NO_VERIFICADO'
    VERIFICADO = 'VERIFICADO'


class UserSchema(BaseModel):
    """
    Defines the pydantic model (schema) for a User
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(default_factory=uuid.uuid4)
    username: str
    email: EmailStr
    phoneNumber: Optional[str] = ""
    dni: Optional[str] = ""
    fullName: Optional[str] = ""

    passwordHash: str
    salt: str
    token: str
    status: UserStatusEnum = Field(default=UserStatusEnum.NO_VERIFICADO)

    expireAt: datetime = Field(default_factory=datetime.now)
    createdAt: datetime = Field(default_factory=datetime.now)
    updateAt: datetime = Field(default_factory=datetime.now)