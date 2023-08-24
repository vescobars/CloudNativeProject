import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4, Field

class RouteBase(BaseModel):
    '''
    Defines the pydantic schema for a given Route
    '''

    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(default_factory=uuid.uuid4)
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: Field(default_factory=datetime.now)
    updateAt: Field(default_factory=datetime.now)