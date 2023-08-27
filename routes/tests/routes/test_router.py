import datetime
import json
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


def gen_planned_start_and_end_date() -> tuple[datetime, datetime]:
    start_date: datetime = gen_plannedStartDate()
    end_date: datetime = gen_plannedEndDate(start_date)
    return start_date, end_date


def gen_plannedStartDate() -> datetime:
    return now_utc() + timedelta(days=random.randint(1, 5))


def gen_plannedEndDate(start_date: datetime) -> datetime:
    return start_date + timedelta(days=random.randint(1, 30))


def create_dummy_route(client: TestClient, faker):
    planned_dates = gen_planned_start_and_end_date()
    planned_start_date = planned_dates[0]
    planned_end_date = planned_dates[1]

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


def test_ping(
        client: TestClient,
        session: Session,
        faker
):
    """

    :param client:
    :param session:
    :param faker:
    :return:
    """
    session.execute(
        delete(Route)
    )
    session.commit()

    response = client.get("/routes/ping")
    assert response.status_code == 200

    response_body = response.text

    assert response_body == "pong"


def test_reset(
        client: TestClient,
        session: Session,
        faker
):
    """

    :param client:
    :param session:
    :param faker:
    :return:
    """
    session.execute(
        delete(Route)
    )
    session.commit()

    # Create 3 dummy routes
    for i in range(3):
        create_dummy_route(client, faker)

    session.commit()

    # Check that 3 routes were created
    row_count_full = session.query(Route).count()

    assert row_count_full == 3

    # Reset DB
    response = client.post("/routes/reset")
    assert response.status_code == 200

    row_count_empty = session.query(Route).count()

    assert row_count_empty == 0


def test_create_route(
        client: TestClient,
        session: Session,
        faker
):
    """
    Tests create route in a perfect scenario with all correct parameters
    Expected result is 201 request code and all field assertions stored in db
    """
    session.execute(
        delete(Route)
    )
    session.commit()

    profile = faker.simple_profile()
    planned_dates = gen_planned_start_and_end_date()
    planned_start_date = planned_dates[0]
    planned_end_date = planned_dates[1]

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
        select(Route).where(Route.id == response_body['id'])
    ).first()[0]

    assert retrieved_route.flightId == payload.flightId
    assert retrieved_route.sourceAirportCode == payload.sourceAirportCode
    assert retrieved_route.destinyAirportCode == payload.destinyAirportCode
    assert retrieved_route.sourceCountry == payload.sourceCountry
    assert retrieved_route.destinyCountry == payload.destinyCountry
    assert retrieved_route.bagCost == payload.bagCost
    assert retrieved_route.plannedStartDate.replace(tzinfo=timezone.utc) == payload.plannedStartDate
    assert retrieved_route.plannedEndDate.replace(tzinfo=timezone.utc) == payload.plannedEndDate


def test_create_route_duplicated_flightId(
        client: TestClient,
        session: Session,
        faker
):
    """
    Tests create route trying to send payload with a duplicated flight id
    Expected result is 412 request code
    """
    session.execute(
        delete(Route)
    )
    session.commit()

    profile = faker.simple_profile()
    planned_dates = gen_planned_start_and_end_date()
    planned_start_date = planned_dates[0]
    planned_end_date = planned_dates[1]

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

    originalFlightId = payload.flightId

    payload_json = payload.model_dump()
    response = client.post("/routes", json=payload_json)
    response_body = response.json()

    assert response.status_code == 201

    retrieved_route = session.execute(
        select(Route).where(Route.id == response_body['id'])
    ).first()[0]

    assert retrieved_route is not None

    # Try to send the same request (with the same flight id)
    duplicated_payload = payload.model_dump()
    response = client.post("/routes", json=duplicated_payload)
    assert response.status_code == 412


def test_create_route_valid_dates(
        client: TestClient,
        session: Session,
        faker
):
    """
    Tests create route where the dates are invalid and before the current date.
    Expected result is  412 code
    """
    session.execute(
        delete(Route)
    )
    session.commit()

    profile = faker.simple_profile()
    wrong_planned_start_date = now_utc() - timedelta(days=random.randint(10, 30))
    wrong_planned_end_date = now_utc() - timedelta(days=random.randint(10, 30))

    payload = CreateRouteRequestSchema(
        flightId=gen_flightId(),
        sourceAirportCode=gen_airportCode(),
        sourceCountry=faker.country(),
        destinyAirportCode=gen_airportCode(),
        destinyCountry=faker.country(),
        bagCost=random.randint(1, 100),
        plannedStartDate=wrong_planned_start_date,
        plannedEndDate=wrong_planned_end_date
    )

    payload_json = payload.model_dump()
    response = client.post("/routes", json=payload_json)
    assert response.status_code == 412


def test_get_route(
        client: TestClient,
        session: Session,
        faker
):
    """
    Tests get route in a perfect scenario with all correct parameters
    Expected result is 200 OK code and returning json with all the specified parameters
    """
    # Clear out information
    session.execute(
        delete(Route)
    )
    session.commit()

    # Create route to return
    planned_dates = gen_planned_start_and_end_date()
    planned_start_date = planned_dates[0]
    planned_end_date = planned_dates[1]

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
    create_response = client.post("/routes", json=payload_json)
    assert create_response.status_code == 201

    create_response_body = create_response.json()
    retrieved_id = create_response_body['id']

    # Searches for the id using get route
    get_response = client.get(f"/routes/{retrieved_id}")
    get_response_body = get_response.json()

    # Check status code is correct
    assert get_response.status_code == 200

    # Assert json content is correct
    assert get_response_body['id'] == retrieved_id
    assert get_response_body['flightId'] == payload.flightId
    assert get_response_body['sourceAirportCode'] == payload.sourceAirportCode
    assert get_response_body['destinyAirportCode'] == payload.destinyAirportCode
    assert get_response_body['sourceCountry'] == payload.sourceCountry
    assert get_response_body['destinyCountry'] == payload.destinyCountry
    assert get_response_body['bagCost'] == payload.bagCost
    assert datetime.fromtimestamp(get_response_body['plannedStartDate']).replace(
        tzinfo=timezone.utc) == payload.plannedStartDate
    assert datetime.fromtimestamp(get_response_body['plannedEndDate']).replace(
        tzinfo=timezone.utc) == payload.plannedEndDate


def test_get_route_invalid_id(
        client: TestClient,
        session: Session,
        faker
):
    """
    Tests get route when the id is invalid
    Expected result is 400 code
    """
    # Clear out information
    session.execute(
        delete(Route)
    )
    session.commit()

    # Searches for the id using get route
    invalid_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(36))
    get_response = client.get(f"/routes/{invalid_id}")
    get_response_body = get_response.json()

    # Check status code is 400 bad request
    assert get_response.status_code == 400


def test_get_route_nonexistent_id(
        client: TestClient,
        session: Session,
        faker
):
    """
    Tests get route when the route searched doesn't exist (id valid, however nonexistent)
    Expected result is 404 code
    """
    # Clear out information
    session.execute(
        delete(Route)
    )
    session.commit()

    # Searches for the id using get route
    nonexistent_uuid = str(uuid.uuid4())
    get_response = client.get(f"/routes/{nonexistent_uuid}")

    # Check status code is 404 route not found request
    assert get_response.status_code == 404


def test_delete_route(
        client: TestClient,
        session: Session,
        faker
):
    """

    :param client:
    :param session:
    :param faker:
    :return:
    """
    session.execute(
        delete(Route)
    )
    session.commit()

    # Create route to be deleted
    planned_dates = gen_planned_start_and_end_date()
    planned_start_date = planned_dates[0]
    planned_end_date = planned_dates[1]

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
    response_body = response.json()
    id_to_delete = response_body['id']

    assert response.status_code == 201

    row_count_full = session.query(Route).count()
    assert row_count_full == 1

    # Create 5 dummy routes
    for i in range(5):
        create_dummy_route(client, faker)

    session.commit()

    # Check that 5 routes were created
    row_count_full = session.query(Route).count()

    assert row_count_full == 6

    # Delete route
    response = client.delete(f"/routes/{id_to_delete}")
    assert response.status_code == 200

    row_count_empty = session.query(Route).count()

    # Check that only 5 routes remain
    assert row_count_empty == 5


def test_delete_route_invalid_id(
        client: TestClient,
        session: Session,
        faker
):
    """
    Tests delete route when the id is invalid
    Expected result is 400 code
    """
    # Clear out information
    session.execute(
        delete(Route)
    )
    session.commit()

    # Searches for the id using get route
    invalid_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(36))
    delete_response = client.delete(f"/routes/{invalid_id}")

    # Check status code is 400 bad request
    assert delete_response.status_code == 400


def test_delete_route_nonexistent_id(
        client: TestClient,
        session: Session,
        faker
):
    """
    Tests delete route when the route doesn't exist (id valid, however nonexistent)
    Expected result is 404 code
    """
    # Clear out information
    session.execute(
        delete(Route)
    )
    session.commit()

    # Tries to delete to delete the id using delete route
    nonexistent_uuid = str(uuid.uuid4())
    delete_response = client.delete(f"/routes/{nonexistent_uuid}")

    # Check status code is 404 route not found request
    assert delete_response.status_code == 404
