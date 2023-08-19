import datetime
import uuid

import pytest
import requests
from fastapi.testclient import TestClient
from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import UserStatusEnum
from src.users.router import create_user
from src.users.schemas import CreateUserRequestSchema


def test_create_user(
        client: TestClient, session: Session, faker
):
    """Checks that POST /users functions correctly and creates the user"""
    session.execute(
        delete(User)
    )
    session.commit()
    profile = faker.simple_profile()
    payload = CreateUserRequestSchema(
        username=profile['username'],
        password=faker.password(),
        email=profile['mail'],
        phoneNumber=faker.phone_number(),
        fullName=profile['name']
    )

    response = client.post("/users", json=payload.model_dump())
    assert response.status_code == 201

    response_body = response.json()
    assert "id" in response_body
    assert "createdAt" in response_body

    retrieved_user = session.execute(
        select(User).where(User.id == response_body['id'])
    ).first()[0]

    assert retrieved_user.username == payload.username
    assert retrieved_user.email == payload.email
    assert retrieved_user.phoneNumber == payload.phoneNumber
    assert retrieved_user.fullName == payload.fullName
    assert retrieved_user.dni is None


def test_create_user_unique_violation(
        client: TestClient, session: Session, faker
):
    """
    Checks that POST /users functions gives a correct response when
    a duplicated email/username is uploaded
    """
    session.execute(
        delete(User)
    )
    session.commit()
    profile = faker.simple_profile()
    payload = CreateUserRequestSchema(
        username=profile['username'],
        password=faker.password(),
        email=profile['mail'],
        phoneNumber=faker.phone_number(),
        dni=profile['name']
    )

    response = client.post("/users", json=payload.model_dump())
    assert response.status_code == 201

    response = client.post("/users", json=payload.model_dump())
    assert response.status_code == 412


def test_create_user_validation_error(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I try to send an invalid request body
    I EXPECT a 400 error
    """
    session.execute(
        delete(User)
    )
    session.commit()
    profile = faker.simple_profile()
    payload = {
        "username": profile['username'],
        "email": profile['mail'],
        "phoneNumber": faker.phone_number(),
        "fullName": profile['name']
    }

    response = client.post("/users", json=payload)
    assert response.status_code == 400


def test_update_user(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I send a new status, fullName, phoneNumber and dni
    I EXPECT a 200 response and the changes to be reflected in database
    """
    session.execute(
        delete(User)
    )
    profile = faker.simple_profile()
    mock_user = User(
        username=profile['username'],
        email=profile['mail'],
        phoneNumber=faker.phone_number(),
        dni=faker.password(),
        fullName=profile['name'],
        passwordHash="a68f7b00815178c7996ddc88208224198a584ce22faf75b19bfeb24ed6f90a59",
        salt="ES25GfW7i4Pp1BqXtASUFXJFe9PMb_7o-2v73v3svWc",
        token="eHBL1jbhBY6GfZ96DC03BlxM38SPF3npRBceefRgnkTpByFexOe7RPPDdLCh9gejD6Fe6Kdl_s5C3Gljqh3WM2xW1IGdlZQYg"
              "V0_v55tw_NB19oMzH2t9AjKycEDdwmqPFJVR4sZuk9MFvSGoY_vQa4Y0pwCvxhBDT1VNsDnQio",
        status=UserStatusEnum.NO_VERIFICADO,
        expireAt=datetime.datetime.now(),
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    session.add(mock_user)
    session.commit()

    second_profile = {
        "status": UserStatusEnum.POR_VERIFICAR,
        "phoneNumber": faker.phone_number(),
        "dni": faker.password(),
        "fullName": faker.name()
    }

    response = client.patch("/users/" + str(mock_user.id),
                            json=second_profile)
    session.flush()
    session.commit()
    assert response.status_code == 200

    response_body = response.json()
    assert "ha sido actualizado" in response_body['msg']

    retrieved_user = session.execute(
        select(User).where(User.id == str(mock_user.id))
    ).scalar_one()

    session.refresh(retrieved_user)

    assert retrieved_user.phoneNumber == second_profile['phoneNumber']
    assert retrieved_user.status == second_profile['status']
    assert retrieved_user.fullName == second_profile['fullName']
    assert retrieved_user.dni == second_profile['dni']


def test_update_user_no_user(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I send a nonexistent UUID
    I EXPECT a 404 response and no changes in DB
    """
    session.execute(
        delete(User)
    )
    profile = faker.simple_profile()
    session.commit()

    second_profile = {
        "status": UserStatusEnum.POR_VERIFICAR,
        "phoneNumber": faker.phone_number(),
        "dni": faker.password(),
        "fullName": faker.name()
    }

    response = client.patch("/users/" + str(uuid.uuid4()),
                            json=second_profile)
    assert response.status_code == 404


def test_gen_token(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I send a valid username and password
    I EXPECT a 200 response and new valid token, with attached ID and expireAt date
    """
    session.execute(
        delete(User)
    )
    profile = faker.simple_profile()
    create_user_payload = CreateUserRequestSchema(
        username=profile['username'],
        password=faker.password(),
        email=profile['mail'],
    )
    mock_user = create_user(create_user_payload, requests.Response(), sess=session)

    credentials = {
        "username": create_user_payload.username,
        "password": create_user_payload.password,
    }

    response = client.post("/users/auth", json=credentials)
    assert response.status_code == 200

    response_body = response.json()
    expireAtTime = datetime.datetime.strptime(response_body['expireAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    assert response_body['id'] == str(mock_user.id)
    assert response_body['token'] is not None
    assert expireAtTime > datetime.datetime.utcnow()

    retrieved_user = session.execute(
        select(User).where(User.id == str(mock_user.id))
    ).scalar_one()

    session.refresh(retrieved_user)

    assert retrieved_user.token == response_body['token']
    assert retrieved_user.expireAt == expireAtTime


@pytest.mark.parametrize("username_suffix", [False, True, None])
def test_gen_token_wrong_pass(
        username_suffix: str, client: TestClient, session: Session, faker
):
    """
    GIVEN I send an invalid username and password, or just an invalid password
    I EXPECT a 404 response
    GIVEN I don't send a username,
    I EXPECT a 400 response
    """
    session.execute(
        delete(User)
    )
    profile = faker.simple_profile()
    create_user_payload = CreateUserRequestSchema(
        username=profile['username'],
        password=faker.password(),
        email=profile['mail'],
    )
    create_user(create_user_payload, requests.Response(), sess=session)
    credentials = {
        "password": faker.password(),
    }
    if username_suffix is not None:
        credentials['username'] = create_user_payload.username if username_suffix else faker.name(),

    response = client.post("/users/auth", json=credentials)

    assert response.status_code == 400 if username_suffix is None else 404


def test_ping(client: TestClient):
    response = client.get("/users/ping")
    assert response.status_code == 200
    assert response.text == 'pong'


def test_reset(
        client: TestClient, session: Session
):
    session.execute(
        delete(User)
    )
    mock_user = User(
        id=uuid.UUID("c62147cf-2e63-4508-b1ff-98f805577f2c"),
        username="user",
        email="user@gmail.com",
        phoneNumber="+57 300 500 2000",
        dni="10100190",
        fullName="Usuario Perez Gómez",
        passwordHash="a68f7b00815178c7996ddc88208224198a584ce22faf75b19bfeb24ed6f90a59",
        salt="ES25GfW7i4Pp1BqXtASUFXJFe9PMb_7o-2v73v3svWc",
        token="eHBL1jbhBY6GfZ96DC03BlxM38SPF3npRBceefRgnkTpByFexOe7RPPDdLCh9gejD6Fe6Kdl_s5C3Gljqh3WM2xW1IGdlZQYg"
              "V0_v55tw_NB19oMzH2t9AjKycEDdwmqPFJVR4sZuk9MFvSGoY_vQa4Y0pwCvxhBDT1VNsDnQio",
        status=UserStatusEnum.NO_VERIFICADO,
        expireAt=datetime.datetime.now(),
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    session.add(mock_user)
    session.commit()
    assert session.scalar(select(func.count()).select_from(User)) == 1, "Table couldn't be set up successfully"
    response = client.post("/users/reset")
    assert response.status_code == 200, "The request failed for an unknown reason"
    assert "los datos fueron eliminados" in str(response.json()['msg'])
    assert session.scalar(select(func.count()).select_from(User)) == 0, "Table reset was unsuccessful"


def test_reset_empty(
        client: TestClient, session: Session
):
    session.execute(
        delete(User)
    )
    session.commit()
    assert session.scalar(select(func.count()).select_from(User)) == 0, "Table couldn't be set up successfully"
    response = client.post("/users/reset")
    assert response.status_code == 200, "The request failed for an unknown reason"
    assert "los datos fueron eliminados" in str(response.json()['msg'])
    assert session.scalar(select(func.count()).select_from(User)) == 0, "Table reset was unsuccessful"
