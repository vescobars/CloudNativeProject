""" SQLAlchemy models for all global entities """

from sqlalchemy import Column, DateTime, UUID, String

from src.database import Base


class CreditCard(Base):
    __tablename__ = "CreditCard"

    id = Column(UUID, primary_key=True, index=True, nullable=False)

    token = Column(String, nullable=False)
    userId = Column(UUID, nullable=False)
    lastFourDigits = Column(String, nullable=False)
    ruv = Column(String, nullable=False)
    issuer = Column(String, nullable=False)
    status = Column(String, nullable=False)

    createdAt = Column(DateTime, nullable=False)
    updateAt = Column(DateTime, nullable=False)
