""" Pydantic schemas for req and response bodies"""
import uuid
from typing import Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, Field, AfterValidator, field_serializer, UUID4

from src.constants import now_utc


def date_validation(d: datetime):
    """Returns value error if date is before the current date"""
    if d < now_utc():
        raise ValueError("Date cannot be before the current date")
    return d


class CreateRouteRequestSchema(BaseModel):
    """
    Request schema used when creating a new route
    """
    flightId: str = Field(min_length=1)
    sourceAirportCode: str = Field(min_length=1)
    sourceCountry: str = Field(min_length=1)
    destinyAirportCode: str = Field(min_length=1)
    destinyCountry: str = Field(min_length=1)
    bagCost: int = Field(ge=0)
    plannedStartDate: datetime = Annotated[datetime, AfterValidator(date_validation)]
    plannedEndDate: datetime = Annotated[datetime, AfterValidator(date_validation)]

    @field_serializer('plannedStartDate', 'plannedEndDate')
    def serialize_dt(self, dt: datetime, _info):
        return dt.timestamp()


def check_uuid4(v: str) -> str:
    """Returns value error if str is not a valid UUID4"""
    uuid.UUID(v)
    return v


class CreateRouteResponseSchema(BaseModel):
    """
    Response schema used when creating a new route
    """
    id: str = Annotated[str, AfterValidator(check_uuid4)]
    createdAt: str

class GetRouteResponseSchema(BaseModel):
    """
    Response schema used when returning a route
    """
    id:  uuid.UUID
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime

    @field_serializer('plannedStartDate', 'plannedEndDate')
    def serialize_dt(self, dt: datetime, _info):
        return dt.timestamp()


