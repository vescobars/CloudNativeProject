from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, Integer, String, Boolean
from .model import Model, Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Offer(Model, Base):
    __tablename__ = 'offers'

    postId = Column(UUID(as_uuid=True), default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), default=uuid.uuid4)
    description = Column(String)
    size = Column(String)
    fragile = Column(Boolean)
    offer = Column(Integer)

    def __init__(
        self, postId, userId,
        description, size, fragile,
        offer
    ):
        Model.__init__(self)
        self.postId = postId
        self.userId = userId
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer


class CreatedOfferSchema(Schema):
    id = fields.UUID()
    userId = fields.UUID()
    createdAt = fields.DateTime()


class OfferDefailtSchema(Schema):
    id = fields.UUID()
    postId = fields.UUID()
    description = fields.Str()
    size = fields.Str()
    fragile = fields.Bool()
    offer = fields.Number()
    createdAt = fields.DateTime()
    userId = fields.UUID()


class OfferSchema(Schema):
    id = fields.UUID()
    postId = fields.UUID()
    description = fields.Str()
    size = fields.Str()
    fragile = fields.Bool()
    offer = fields.Number()
    userId = fields.UUID()
    createdAt = fields.DateTime()
