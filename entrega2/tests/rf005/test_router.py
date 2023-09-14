from fastapi.testclient import TestClient
from httmock import HTTMock

from tests.rf004.mocks import mock_success_auth
from tests.rf005.mocks import mock_success_search_offers, mock_success_get_route, mock_success_get_post

BASE_ROUTE = "/rf005"
BASE_AUTH_TOKEN = "Bearer 3d91ee00503447c58e1787a90beaa265"


def test_rf005(
        client: TestClient
):
    """Checks that POST /rf004 functions correctly and creates the offer"""

    with HTTMock(
            mock_success_auth, mock_success_search_offers, mock_success_get_post,
            mock_success_get_route
    ):
        response = client.get(
            f"{BASE_ROUTE}/posts/68158796-9594-4b4f-a184-8df97379e912",
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 200

        response_body = response.json()
        assert "data" in response_body
        assert "msg" in response_body

        assert response_body["data"]["id"] == "a8ae58c4-1d41-4d3c-a3f8-f941906779b4"
        assert response_body["data"]["userId"] == "cdab3f90-f8d8-458c-8447-ac8764f8e471"
        assert response_body["data"]["postId"] == "86864ea3-69ed-4fca-9158-44c15a1e61a9"


def test_ping(client: TestClient):
    response = client.get(f"{BASE_ROUTE}/ping")
    assert response.status_code == 200
    assert response.text == 'pong'
