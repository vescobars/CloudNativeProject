from fastapi.testclient import TestClient
from httmock import HTTMock

from tests.rf004.mocks import mock_success_auth, mock_success_get_post, \
    mock_success_create_utility, mock_success_get_route, mock_success_post_offer, mock_forbidden_auth, mock_failed_auth

BASE_ROUTE = "/rf004"
BASE_AUTH_TOKEN = "Bearer 3d91ee00503447c58e1787a90beaa265"

BASIC_PAYLOAD = {
    "description": "Example description",
    "size": "SMALL",
    "fragile": True,
    "offer": 400.0
}

def test_rf004(
        client: TestClient
):
    """Checks that POST /rf004 functions correctly and creates the offer"""


    with HTTMock(
            mock_success_auth, mock_success_get_post, mock_success_get_route,
            mock_success_post_offer, mock_success_create_utility
    ):
        response = client.post(
            f"{BASE_ROUTE}/posts/86864ea3-69ed-4fca-9158-44c15a1e61a9/offers", json=BASIC_PAYLOAD,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 201

        response_body = response.json()
        assert "data" in response_body
        assert "msg" in response_body

        assert response_body["data"]["id"] == "a8ae58c4-1d41-4d3c-a3f8-f941906779b4"
        assert response_body["data"]["userId"] == "cdab3f90-f8d8-458c-8447-ac8764f8e471"
        assert response_body["data"]["postId"] == "86864ea3-69ed-4fca-9158-44c15a1e61a9"


def test_rf004_no_credential(
        client: TestClient
):
    """Checks that POST /rf004 returns 403 when no credentials are given"""

    with HTTMock(
            mock_forbidden_auth
    ):
        response = client.post(
            f"{BASE_ROUTE}/posts/86864ea3-69ed-4fca-9158-44c15a1e61a9/offers", json=BASIC_PAYLOAD)
        assert response.status_code == 403


def test_rf004_rejected_credential(
        client: TestClient
):
    """Checks that POST /rf004 returns 401 when credentials are valid but unauthorized"""

    with HTTMock(
            mock_failed_auth
    ):
        response = client.post(
            f"{BASE_ROUTE}/posts/86864ea3-69ed-4fca-9158-44c15a1e61a9/offers", json=BASIC_PAYLOAD,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 401


def test_ping(client: TestClient):
    response = client.get(f"{BASE_ROUTE}/ping")
    assert response.status_code == 200
    assert response.text == 'pong'
