import datetime
import uuid
from fastapi.testclient import TestClient
from httmock import HTTMock
from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session

from src.models import CreditCard
from tests.mocks import mock_success_auth, mock_forbidden_auth

BASE_ROUTE = "/credit-cards/"
BASE_AUTH_TOKEN = "Bearer 3d91ee00503447c58e1787a90beaa265"


def test_create_utility(
        client: TestClient, session: Session
):
    """Checks that POST /utility functions correctly and creates the utility"""
    session.execute(
        delete(CreditCard)
    )
    session.commit()
    payload = {
        "cardNumber": "1111222233334444",
        "cvv": "123",
        "expirationDate": "12/25",
        "cardHolderName": "Juan Perez"
    }
    with HTTMock(mock_success_auth):
        response = client.post(BASE_ROUTE, json=payload, headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        assert response.status_code == 201

        response_body = response.json()
        assert "offer_id" in response_body
        assert "createdAt" in response_body

        retrieved_card = session.execute(
            select(CreditCard).where(str(CreditCard.id) == response_body['id'])
        ).scalar()

        assert retrieved_card is not None

def test_ping(client: TestClient):
    response = client.get("/credit-cards/ping")
    assert response.status_code == 200
    assert response.text == 'pong'


def test_reset(
        client: TestClient, session: Session
):
    session.execute(
        delete(CreditCard)
    )
    # mock_utility = CreditCard(
    #     token="",
    #     userId="1234",
    #     lastFourDigits="9876",
    #     ruv= ,
    #     issuer= ,
    #     status= ,
    #     createdAt= datetime.datetime.now(),
    #     updateAt= datetime.datetime.now()
    # )
    # session.add(mock_utility)
    session.commit()
    assert session.scalar(select(func.count()).select_from(CreditCard)) == 1, "Table couldn't be set up successfully"
    response = client.post("/credit-cards/reset")
    assert response.status_code == 200, "The request failed for an unknown reason"
    assert session.scalar(select(func.count()).select_from(CreditCard)) == 0, "Table reset was unsuccessful"


def test_reset_empty(
        client: TestClient, session: Session
):
    session.execute(
        delete(Utility)
    )
    session.commit()
    assert session.scalar(select(func.count()).select_from(Utility)) == 0, "Table couldn't be set up successfully"
    response = client.post("/utility/reset")
    assert response.status_code == 200, "The request failed for an unknown reason"
    assert "los datos fueron eliminados" in str(response.json()['msg'])
    assert session.scalar(select(func.count()).select_from(Utility)) == 0, "Table reset was unsuccessful"
