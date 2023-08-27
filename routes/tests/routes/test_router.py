import datetime
import uuid
import itertools
import random
import string

import pytest
import requests
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session

from src.models import Route
from src.routes.router import create_route
from src.routes.schemas import CreateRouteRequestSchema
from src.constants import now_utc


def gen_flightId() -> str:
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(6))


def gen_airportCode() -> str:
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(3))


def test_create_route(
        client: TestClient,
        session: Session,
        faker
):
    """"""
    session.execute(
        delete(Route)
    )
    session.commit()

    profile = faker.simple_profile()
    planned_start_date = now_utc()
    planned_end_date = (now_utc() + timedelta(days=random.randint(1, 30)))

    payload = CreateRouteRequestSchema(
        flightId=gen_flightId(),
        sourceAirportCode=gen_airportCode(),
        sourceCountry=faker.country(),
        destinyAirportCode=gen_airportCode(),
        destinyCountry=faker.country(),
        bagCost=random.randint(1, 100),
        plannedStartDate=planned_start_date,
        plannedEndDate=planned_end_date
    )

    payload_json = payload.model_dump()
    response = client.post("/routes", json=payload_json)
    assert response.status_code == 201

    response_body = response.json()
    retrieved_route = session.execute(
        select(Route).where(Route.id == response_body['id'] )
    ).first()[0]


    assert retrieved_route.flightId == payload.flightId
    assert retrieved_route.sourceAirportCode == payload.sourceAirportCode
    assert retrieved_route.destinyAirportCode == payload.destinyAirportCode
    assert retrieved_route.sourceCountry == payload.sourceCountry
    assert retrieved_route.destinyCountry == payload.destinyCountry
    assert retrieved_route.bagCost == payload.bagCost
    assert retrieved_route.plannedStartDate.replace(tzinfo=timezone.utc) == payload.plannedStartDate
    assert retrieved_route.plannedEndDate.replace(tzinfo=timezone.utc) == payload.plannedEndDate
