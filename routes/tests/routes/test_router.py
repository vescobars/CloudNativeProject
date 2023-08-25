import datetime
import uuid
import itertools
import random
import string

import pytest
import requests
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session

from src.models import Route
from src.routes.router import create_route
from src.routes.schemas import CreateRouteRequestSchema
from src.constants import now_utc


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
    payload = CreateRouteRequestSchema(
        flightId=lambda length=6: ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length)),
        sourceAirportCode=lambda: [''.join(combination) for combination in
                                   itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=3)],
        sourceCountry=faker.country(),
        destinyAirportCode=lambda: [''.join(combination) for combination in
                                    itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=3)],
        destinyCountry=faker.country(),
        bagCost=random.randint(1, 100),
        plannedStartDate=now_utc(),
        plannedEndDate=now_utc() + timedelta(days=random.randint(1, 30))
    )

    response_body = client.post("/routers", json=payload.model_dump())
    assert response.status_code == 201

    retrieved_route = session.execute(
        select(Route).where(Route.id == response_body['id'])
    ).first()[0]

    assert retrieved_route.flightId == payload.flightId
    assert retrieved_route.sourceAirportCode == payload.sourceAirportCode
    assert retrieved_route.destinyAirportCode == payload.destinyAirportCode
    assert retrieved_route.sourceCountry == payload.sourceCountry
    assert retrieved_route.destinyCountry == payload.destinyCountry
    assert retrieved_route.bagCost == payload.bagCost
    assert retrieved_route.plannedStartDate == payload.plannedStartDate
    assert retrieved_route.plannedEndDate == payload.plannedEndDate
