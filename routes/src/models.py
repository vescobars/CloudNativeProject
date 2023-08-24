""" SQLAlchemy models for all global entities """

import uuid

from sqlalchemy import Column,String, UUID, Integer, DateTime

from src.database import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(UUID, primary_key=True, index=True, nullable=False, default=uuid.uuid4() )
    flightId = Column(String, unique=True, index=True, nullable=False)
    sourceAirportCode = Column(String, index=True, nullable=False) #IATA Airport code system
    sourceCountry = Column(String,index=True, nullable=False)
    destinyAirportCode = Column(String, index=True, nullable=False)
    destinyCountry = Column(String,index=True, nullable=False)
    bagCost = Column(Integer,nullable=False)
    plannedStartDate = Column(DateTime, nullable=False)
    plannedEndDate = Column(DateTime, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updateAt = Column(DateTime, nullable=False)
