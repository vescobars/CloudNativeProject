from fastapi.testclient import TestClient
from httmock import HTTMock

from src.schemas import BagSize
from tests.rf004.mocks import mock_success_auth
from tests.rf005.mocks import mock_success_search_offers, mock_success_get_route, mock_success_get_post, \
    mock_success_search_utilities, mock_success_get_post_different_owner, mock_failed_get_post_not_found

BASE_ROUTE = "/rf005"
BASE_AUTH_TOKEN = "Bearer 3d91ee00503447c58e1787a90beaa265"


def test_rf005(
        client: TestClient
):
    """Checks that GET /rf005 functions correctly and returns the post with the route embedded, and
    a filtered list of offers, sorted in descending order by utility score"""

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

        # Verify descending order of utility
        prev_utility_calculated = 9999999999999
        prev_utility_observed = 9999999999999
        for i in range(0, len(offers_list)):
            current_utility_calculated = get_utility(
                offers_list[i]["offer"],
                offers_list[i]["size"],
                40,
            )
            assert current_utility_calculated == float(offers_list[i]["score"])

            assert current_utility_calculated < prev_utility_calculated
            assert float(offers_list[i]["score"]) < prev_utility_observed

            prev_utility_calculated = current_utility_calculated
            prev_utility_observed = float(offers_list[i]["score"])


def test_rf005_post_not_found(
        client: TestClient
):
    """Checks that GET /rf005 Fails correctly if the post doesn't actually exist"""

    with HTTMock(
            mock_success_auth, mock_failed_get_post_not_found
    ):
        response = client.get(
            f"{BASE_ROUTE}/posts/3fa8eb34-5e79-4daf-aba7-84c007ff0445",
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 404


def test_rf005_not_post_owner(
        client: TestClient
):
    """Checks that GET /rf005 Fails correctly if the user is not the owner of the post"""

    with HTTMock(
            mock_success_auth, mock_success_get_post_different_owner
    ):
        response = client.get(
            f"{BASE_ROUTE}/posts/68158796-9594-4b4f-a184-8df97379e912",
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 403


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
