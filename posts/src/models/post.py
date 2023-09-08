from marshmallow import Schema, fields
from sqlalchemy import Column, DateTime, Integer, Integer
from .model import Model, Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Post(Model, Base):
    __tablename__ = 'posts'

    routeId = Column(UUID(as_uuid=True), default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), default=uuid.uuid4)
    expireAt = Column(DateTime)

    def __init__(self, routeId, userId, expireAt):
        Model.__init__(self)
        self.routeId = routeId
        self.userId = userId
        self.expireAt = expireAt


class CreatedPostSchema(Schema):
    id = fields.UUID()
    userId = fields.UUID()
    createdAt = fields.DateTime()


class PostSchema(Schema):
    id = fields.UUID()
    routeId = fields.UUID()
    userId = fields.UUID()
    expireAt = fields.DateTime()
    createdAt = fields.DateTime()
