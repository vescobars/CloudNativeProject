""" Pydantic schemas for req and response bodies"""
import uuid
from typing import Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, Field, AfterValidator


def date_validation(d: datetime):
    """Returns value error if date is before the current date"""
    current_date = datetime.now()
    if d < current_date:
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
