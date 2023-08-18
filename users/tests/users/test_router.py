import datetime
import uuid

from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import UserStatusEnum
from src.users.schemas import CreateUserRequestSchema


def test_create_user(
        client: TestClient, session: Session, faker
):
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


    retrieved_user = session.execute(select(User).where(User.id == response_body['id'])).first()[0]

    assert retrieved_user.username == payload.username
    assert retrieved_user.email == payload.email
    assert retrieved_user.phoneNumber == payload.phoneNumber
    assert retrieved_user.fullName == payload.fullName
    assert retrieved_user.dni is None


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
