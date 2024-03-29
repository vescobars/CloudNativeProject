import datetime
import uuid
from fastapi.testclient import TestClient
from httmock import HTTMock
from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session

from src.models import Utility
from tests.mocks import mock_success_auth, mock_forbidden_auth

BASE_ROUTE = "/utility/"
BASE_AUTH_TOKEN = "Bearer 3d91ee00503447c58e1787a90beaa265"


def test_create_utility(
        client: TestClient, session: Session
):
    """Checks that POST /utility functions correctly and creates the utility"""
    session.execute(
        delete(Utility)
    )
    session.commit()
    payload = {
        "offer_id": "3d747856-5ddb-467e-b9f4-2c7e2ef19245",
        "offer": 400.5,
        "size": "MEDIUM",
        "bag_cost": 60
    }
    with HTTMock(mock_success_auth):
        response = client.post(BASE_ROUTE, json=payload, headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        assert response.status_code == 201

        response_body = response.json()
        assert "offer_id" in response_body
        assert "createdAt" in response_body

        retrieved_utility = session.execute(
            select(Utility).where(Utility.offer_id == response_body['offer_id'])
        ).scalar()

        assert str(retrieved_utility.offer_id) == payload["offer_id"]
        assert retrieved_utility.utility == 400.5 - (0.5 * 60)


def test_create_utility_no_credentials(
        client: TestClient, session: Session
):
    """Checks that POST /utility rejects a request with invalid credentials"""
    session.execute(
        delete(Utility)
    )
    session.commit()
    payload = {
        "offer_id": "3d747856-5ddb-467e-b9f4-2c7e2ef19245",
        "offer": 400.5,
        "size": "MEDIUM",
        "bag_cost": 60
    }
    response = client.post(BASE_ROUTE, json=payload)
    assert response.status_code == 403


def test_create_utility_forbidden(
        client: TestClient, session: Session
):
    """Checks that POST /utility rejects a request with forbidden credentials"""
    session.execute(
        delete(Utility)
    )
    session.commit()
    payload = {
        "offer_id": "3d747856-5ddb-467e-b9f4-2c7e2ef19245",
        "offer": 400.5,
        "size": "MEDIUM",
        "bag_cost": 60
    }
    with HTTMock(mock_forbidden_auth):
        response = client.post(BASE_ROUTE, json=payload, headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        assert response.status_code == 401


def test_create_utility_unique_violation(
        client: TestClient, session: Session, faker
):
    """
    Checks that POST /utility functions gives a correct response when
    a duplicated offer_id is uploaded
    """
    session.execute(
        delete(Utility)
    )
    session.commit()
    payload = {
        "offer_id": "3d747856-5ddb-467e-b9f4-2c7e2ef19245",
        "offer": 400.5,
        "size": "MEDIUM",
        "bag_cost": 60
    }
    with HTTMock(mock_success_auth):
        response = client.post(BASE_ROUTE, json=payload, headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        assert response.status_code == 201

        response2 = client.post(BASE_ROUTE, json=payload, headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        assert response2.status_code == 412


def test_create_utility_validation_error(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I try to send an invalid request body
    I EXPECT a 400 error
    """
    session.execute(
        delete(Utility)
    )
    session.commit()
    payload = {
        "offer_id": "3d747856-5ddb-467e-b9f4-2c7e2ef19245",
        "offer": 400.5,
        "size": "500",
        "bag_cost": 60
    }
    with HTTMock(mock_success_auth):
        response = client.post(BASE_ROUTE, json=payload, headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        assert response.status_code == 400


def test_update_utility(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I send new offer value, bagsize or bag_cost and a valid offer_id
    I EXPECT a 200 response and the new utility to be reflected in database
    """
    session.execute(
        delete(Utility)
    )
    mock_utility = Utility(
        offer_id=uuid.UUID("c62147cf-2e63-4508-b1ff-98f805577f2c"),
        utility=400.2,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    session.add(mock_utility)
    session.commit()

    second_utility = {
        "offer_id": "c62147cf-2e63-4508-b1ff-98f805577f2c",
        "offer": 400.5,
        "size": "MEDIUM",
        "bag_cost": 60
    }
    with HTTMock(mock_success_auth):
        response = client.patch(BASE_ROUTE + str(mock_utility.offer_id),
                                json=second_utility, headers={
                "Authorization": BASE_AUTH_TOKEN
            })
        session.flush()
        session.commit()
        assert response.status_code == 200

        response_body = response.json()
        assert "ha sido actualizada" in response_body['msg']

        retrieved_utility = session.execute(
            select(Utility).where(Utility.offer_id == str(mock_utility.offer_id))
        ).scalar_one()

        session.refresh(retrieved_utility)

        assert str(retrieved_utility.offer_id) == second_utility['offer_id']
        assert retrieved_utility.utility == second_utility["offer"] - (0.5 * second_utility["bag_cost"])


def test_update_utility_no_utility(
        client: TestClient, session: Session
):
    """
    GIVEN I send a nonexistent offer_id UUID
    I EXPECT a 404 response and no changes in DB
    """
    session.execute(
        delete(Utility)
    )

    second_utility = {
        "offer_id": "c62147cf-2e63-4508-b1ff-98f805577f2c",
        "offer": 400.5,
        "size": "MEDIUM",
        "bag_cost": 60
    }
    with HTTMock(mock_success_auth):
        response = client.patch(BASE_ROUTE + str(uuid.uuid4()),
                                json=second_utility, headers={
                "Authorization": BASE_AUTH_TOKEN
            })
        assert response.status_code == 404


def test_update_utility_invalid_request(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I send an empty body
    I EXPECT a 400 response and no changes in DB
    """
    session.execute(
        delete(Utility)
    )

    second_utility = {}
    with HTTMock(mock_success_auth):
        response = client.patch(BASE_ROUTE + str(uuid.uuid4()),
                                json=second_utility, headers={
                "Authorization": BASE_AUTH_TOKEN
            })
    assert response.status_code == 400


def test_get_utility(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I send a valid token and offer_id
    I EXPECT a 200 response and all utility fields
    """
    session.execute(
        delete(Utility)
    )
    mock_utility = Utility(
        offer_id=uuid.UUID("c62147cf-2e63-4508-b1ff-98f805577f2c"),
        utility=400.2,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    session.add(mock_utility)
    session.commit()

    with HTTMock(mock_success_auth):
        response = client.get(BASE_ROUTE + str(mock_utility.offer_id), headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        session.flush()
        session.commit()
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["offer_id"] == str(mock_utility.offer_id)
        assert response_body["utility"] == mock_utility.utility


def test_get_utility_not_found(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I send a valid token and a nonexistent offer_id
    I EXPECT a 404 response
    """
    session.execute(
        delete(Utility)
    )

    with HTTMock(mock_success_auth):
        response = client.get("/utility/cdab3f90-f8d8-458c-8447-ac8764f8e471", headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        session.flush()
        session.commit()
        assert response.status_code == 404


def test_delete_utility(
        client: TestClient, session: Session, faker
):
    """
    GIVEN I send a valid token and offer_id
    I EXPECT a 200 response and the offer id
    """
    session.execute(
        delete(Utility)
    )
    mock_utility = Utility(
        offer_id=uuid.UUID("c62147cf-2e63-4508-b1ff-98f805577f2c"),
        utility=400.2,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    session.add(mock_utility)
    session.commit()

    with HTTMock(mock_success_auth):
        response = client.delete(BASE_ROUTE + str(mock_utility.offer_id), headers={
            "Authorization": BASE_AUTH_TOKEN
        })
        session.flush()
        session.commit()
        assert response.status_code == 200

        response_body = response.json()

        assert response_body["deleted_offer_id"] == str(mock_utility.offer_id)

        retrieved_utility = session.execute(
            select(Utility).where(Utility.offer_id == str(mock_utility.offer_id))
        ).scalar()
        assert retrieved_utility is None


def test_get_utilities(
        client: TestClient, session: Session
):
    """
    GIVEN I send a valid token and offer_ids
    I EXPECT a 200 response and all utilities in descending order by utility score
    """
    session.execute(
        delete(Utility)
    )
    mock_utility_1 = Utility(
        offer_id=uuid.uuid4(),
        utility=250,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    mock_utility_2 = Utility(
        offer_id=uuid.uuid4(),
        utility=126.90,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    mock_utility_3 = Utility(
        offer_id=uuid.uuid4(),
        utility=7200.5,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    mock_utility_4 = Utility(
        offer_id=uuid.uuid4(),
        utility=12.33,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    mock_utility_5 = Utility(
        offer_id=uuid.uuid4(),
        utility=12.33,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    session.add(mock_utility_1)
    session.add(mock_utility_2)
    session.add(mock_utility_3)
    session.add(mock_utility_4)
    session.add(mock_utility_5)
    session.commit()

    with HTTMock(mock_success_auth):
        canary_uuid = uuid.uuid4()
        response = client.post(
            BASE_ROUTE + "list",
            headers={
                "Authorization": BASE_AUTH_TOKEN
            },
            json=[
                str(mock_utility_2.offer_id),
                str(mock_utility_1.offer_id),
                str(canary_uuid),
                str(mock_utility_4.offer_id),
                str(mock_utility_3.offer_id),
            ]
        )

        session.flush()
        session.commit()
        assert response.status_code == 200

        response_body: list = response.json()
        assert len(response_body) == 4
        for elem in response_body:
            assert elem["offer_id"] != str(canary_uuid)
            assert elem["offer_id"] != str(mock_utility_5.offer_id)

        assert response_body[0]["offer_id"] == str(mock_utility_3.offer_id)
        assert response_body[3]["offer_id"] == str(mock_utility_4.offer_id)


def test_ping(client: TestClient):
    response = client.get("/utility/ping")
    assert response.status_code == 200
    assert response.text == 'pong'


def test_reset(
        client: TestClient, session: Session
):
    session.execute(
        delete(Utility)
    )
    mock_utility = Utility(
        offer_id=uuid.UUID("c62147cf-2e63-4508-b1ff-98f805577f2c"),
        utility=400.2,
        createdAt=datetime.datetime.now(),
        updateAt=datetime.datetime.now()
    )
    session.add(mock_utility)
    session.commit()
    assert session.scalar(select(func.count()).select_from(Utility)) == 1, "Table couldn't be set up successfully"
    response = client.post("/utility/reset")
    assert response.status_code == 200, "The request failed for an unknown reason"
    assert "los datos fueron eliminados" in str(response.json()['msg'])
    assert session.scalar(select(func.count()).select_from(Utility)) == 0, "Table reset was unsuccessful"


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
