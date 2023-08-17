import datetime
import uuid

from fastapi.testclient import TestClient
from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import UserStatusEnum


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
