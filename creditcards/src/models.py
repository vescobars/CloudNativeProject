""" SQLAlchemy models for all global entities """

from sqlalchemy import Column, DateTime, UUID, Float

from src.database import Base


class Utility(Base):
    __tablename__ = "utility"

    offer_id = Column(UUID, primary_key=True, index=True, nullable=False)
    utility = Column(Float, nullable=False)

    createdAt = Column(DateTime, nullable=False)
    updateAt = Column(DateTime, nullable=False)
