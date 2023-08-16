""" SQLAlchemy models for all global entities """

import uuid

from sqlalchemy import Column, String, DateTime, UUID

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, nullable=False, default=uuid.uuid4())
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phoneNumber = Column(String)
    dni = Column(String)
    fullName = Column(String)

    passwordHash = Column("password", String, nullable=False)
    salt = Column(String, nullable=False)
    token = Column(String)
    status = Column(String, nullable=False)

    expireAt = Column(DateTime, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updateAt = Column(DateTime, nullable=False)
