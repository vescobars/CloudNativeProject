import uuid

from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID, primary_key=True, index=True, nullable=False, default=uuid.uuid4())
    routeId = Column(UUID, primary_key=False, index=True, nullable=False, default=uuid.uuid4())
    userId = Column(UUID, primary_key=False, index=True, nullable=False, default=uuid.uuid4())
    expireAt = Column(DateTime, index=True, nullable=False) 
    createdAt = Column(DateTime, index=False, nullable=False, default=func.now())