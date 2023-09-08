from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime, Integer
from .model import Model, Base


class Route(Model, Base):
    __tablename__ = 'routes'

    flightId = Column(String)
    sourceAirportCode = Column(String)
    sourceCountry = Column(String)
    destinyAirportCode = Column(String)
    destinyCountry = Column(String)
    bagCost = Column(Integer)
    plannedStartDate = Column(DateTime)
    plannedEndDate = Column(DateTime)

    def __init__(
        self, flightId, sourceAirportCode, sourceCountry,
        destinyAirportCode, destinyCountry, bagCost,
        plannedStartDate, plannedEndDate
    ):
        Model.__init__(self)
        self.flightId = flightId
        self.sourceAirportCode = sourceAirportCode
        self.sourceCountry = sourceCountry
        self.destinyAirportCode = destinyAirportCode
        self.destinyCountry = destinyCountry
        self.bagCost = bagCost
        self.plannedStartDate = plannedStartDate
        self.plannedEndDate = plannedEndDate


class CreatedRouteSchema(Schema):
    id = fields.UUID()
    createdAt = fields.DateTime()


class RouteSchema(Schema):
    id = fields.UUID()
    flightId = fields.Str()
    sourceAirportCode = fields.Str()
    sourceCountry = fields.Str()
    destinyAirportCode = fields.Str()
    destinyCountry = fields.Str()
    bagCost = fields.Number()
    plannedStartDate = fields.DateTime()
    plannedEndDate = fields.DateTime()
    createdAt = fields.DateTime()
