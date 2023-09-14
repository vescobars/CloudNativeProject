from fastapi.testclient import TestClient
from httmock import HTTMock

from src.schemas import BagSize
from tests.rf004.mocks import mock_success_auth
from tests.rf005.mocks import mock_success_search_offers, mock_success_get_route, mock_success_get_post, \
    mock_success_search_utilities

BASE_ROUTE = "/rf005"
BASE_AUTH_TOKEN = "Bearer 3d91ee00503447c58e1787a90beaa265"


def test_rf005(
        client: TestClient
):
    """Checks that POST /rf004 functions correctly and creates the offer"""

    with HTTMock(
            mock_success_auth, mock_success_search_offers, mock_success_get_post,
            mock_success_get_route, mock_success_search_utilities
    ):
        response = client.get(
            f"{BASE_ROUTE}/posts/68158796-9594-4b4f-a184-8df97379e912",
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 200

        response_body = response.json()
        assert "data" in response_body

        assert response_body["data"]["id"] == "68158796-9594-4b4f-a184-8df97379e912"

        assert "plannedStartDate" in response_body["data"]
        assert "plannedEndDate" in response_body["data"]
        assert "createdAt" in response_body["data"]
        assert "expireAt" in response_body["data"]

        offers_list = response_body["data"]["offers"]
        assert len(offers_list) == 4

        temp_utility = 9999999999999
        for i in range(0, len(offers_list)):
            # Verify descending order of utility
            assert offers_list[i] < temp_utility
            temp_utility = get_utility(
                offers_list[i]["offer"],
                offers_list[i]["size"],
                40,
            )


def test_ping(client: TestClient):
    response = client.get(f"{BASE_ROUTE}/ping")
    assert response.status_code == 200
    assert response.text == 'pong'


def get_utility(offer_raw: str, size_raw: str, bag_cost: int) -> float:
    """Calculates utility score"""
    offer = float(offer_raw)
    size = BagSize(size_raw)

    bag_occupation = 1.0
    if size == BagSize.MEDIUM:
        bag_occupation = 0.5
    if size == BagSize.SMALL:
        bag_occupation = 0.25
    return offer - (bag_occupation * float(bag_cost))
