from fastapi.testclient import TestClient
from httmock import HTTMock
from tests.rf003.mocks import mock_success_auth, mock_forbidden_auth, mock_failed_auth, mock_success_get_routes, \
    mock_success_get_posts_empty_response, mock_success_create_post, mock_success_create_route, \
    mock_success_get_routes_empty_response, mock_success_get_posts, mock_failed_create_post

BASE_ROUTE = "/rf003"
BASE_AUTH_TOKEN = "Bearer 3d91ee00503447c58e1787a90beaa265"

BASIC_PAYLOAD = {
    "flightId": "abcdfghijklm",
    "expireAt": "2023-10-10T21:20:53.214Z",
    "plannedStartDate": "2023-10-13T21:20:50.214Z",
    "plannedEndDate": "2023-10-14T21:20:54.214Z",
    "origin": {
        "airportCode": "KJFK",
        "country": "USA"
    },
    "destiny": {
        "airportCode": "KDFW",
        "country": "USA"
    },
    "bagCost": 100
}


def test_rf003_no_credential(
        client: TestClient
):
    """Checks that POST /rf003 returns 403 when no credentials are given"""

    with HTTMock(
            mock_forbidden_auth
    ):
        response = client.post(
            f"{BASE_ROUTE}/posts", json=BASIC_PAYLOAD)
        assert response.status_code == 403


def test_rf003_rejected_credential(
        client: TestClient
):
    """Checks that POST /rf003 returns 401 when credentials are valid but unauthorized"""

    with HTTMock(
            mock_failed_auth
    ):
        response = client.post(
            f"{BASE_ROUTE}/posts", json=BASIC_PAYLOAD,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 401


def test_start_date_not_consistent_now(
        client: TestClient
):
    """Checks that POST /rf003 returns 412 when the plannedStartDate is before now"""

    with HTTMock(
            mock_success_auth
    ):
        payload = {
            "flightId": "abcdfghijklm",
            "expireAt": "2023-10-10T21:20:53.214Z",
            "plannedStartDate": "2021-10-10T21:20:50.214Z",
            "plannedEndDate": "2023-10-11T21:20:54.214Z",
            "origin": {
                "airportCode": "KJFK",
                "country": "USA"
            },
            "destiny": {
                "airportCode": "KDFW",
                "country": "USA"
            },
            "bagCost": 100
        }
        response = client.post(
            f"{BASE_ROUTE}/posts", json=payload,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 412

        response_body = response.json()
        assert "msg" in response_body

        assert response_body["msg"] == "Las fechas del trayecto no son válidas"


def test_end_date_not_consistent_now(
        client: TestClient
):
    """Checks that POST /rf003 returns 412 when the plannedEndDate is before now"""

    with HTTMock(
            mock_success_auth
    ):
        payload = {
            "flightId": "abcdfghijklm",
            "expireAt": "2023-10-10T21:20:53.214Z",
            "plannedStartDate": "2023-10-10T21:20:50.214Z",
            "plannedEndDate": "2021-10-11T21:20:54.214Z",
            "origin": {
                "airportCode": "KJFK",
                "country": "USA"
            },
            "destiny": {
                "airportCode": "KDFW",
                "country": "USA"
            },
            "bagCost": 100
        }
        response = client.post(
            f"{BASE_ROUTE}/posts", json=payload,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 412

        response_body = response.json()
        assert "msg" in response_body

        assert response_body["msg"] == "Las fechas del trayecto no son válidas"


def test_expire_date_not_consistent_now(
        client: TestClient
):
    """Checks that POST /rf003 returns 412 when the expireAt date is before now"""

    with HTTMock(
            mock_success_auth
    ):
        payload = {
            "flightId": "abcdfghijklm",
            "expireAt": "2021-09-30T21:20:53.214Z",
            "plannedStartDate": "2023-10-10T21:20:50.214Z",
            "plannedEndDate": "2023-10-11T21:20:54.214Z",
            "origin": {
                "airportCode": "KJFK",
                "country": "USA"
            },
            "destiny": {
                "airportCode": "KDFW",
                "country": "USA"
            },
            "bagCost": 100
        }
        response = client.post(
            f"{BASE_ROUTE}/posts", json=payload,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 412

        response_body = response.json()
        assert "msg" in response_body

        assert response_body["msg"] == "La fecha expiración no es válida"


def test_expire_date_not_consistent_start(
        client: TestClient
):
    """Checks that POST /rf003 returns 412 when the expireAt date is after start plannedStartDate"""

    with HTTMock(
            mock_success_auth
    ):
        payload = {
            "flightId": "abcdfghijklm",
            "expireAt": "2023-10-10T21:20:53.214Z",
            "plannedStartDate": "2023-09-30T21:20:50.214Z",
            "plannedEndDate": "2023-11-11T21:20:54.214Z",
            "origin": {
                "airportCode": "KJFK",
                "country": "USA"
            },
            "destiny": {
                "airportCode": "KDFW",
                "country": "USA"
            },
            "bagCost": 100
        }
        response = client.post(
            f"{BASE_ROUTE}/posts", json=payload,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 412

        response_body = response.json()
        assert "msg" in response_body

        assert response_body["msg"] == "La fecha expiración no es válida"


def test_rf003_get_route_success(
        client: TestClient
):
    """Checks that POST /rf003 functions correctly and creates the post when the route already exists"""

    with HTTMock(
            mock_success_auth,
            mock_success_get_routes,
            mock_success_get_posts_empty_response,
            mock_success_create_post
    ):
        response = client.post(
            f"{BASE_ROUTE}/posts", json=BASIC_PAYLOAD,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 201

        response_body = response.json()
        assert "data" in response_body
        assert "msg" in response_body

        assert response_body["data"]["id"] != ""
        assert response_body["data"]["id"] is not None
        assert response_body["data"]["userId"] == "ab99beb5-37e7-4e85-87e2-3578f92d883c"
        assert response_body["data"]["createdAt"] == "2023-10-05T21:20:53.214Z"
        assert response_body["data"]["expireAt"] == "2023-10-10T21:20:53.214Z"
        assert response_body["data"]["route"]["id"] == "a8ae58c4-1d41-4d3c-a3f8-f941906779b4"
        assert response_body["data"]["route"]["createdAt"] == "2023-09-25T21:20:54.214Z"


def test_rf003_create_route_success(
        client: TestClient
):
    """Checks that POST /rf003 functions correctly and creates the post and the route, when the route does not exist"""

    with HTTMock(
            mock_success_auth,
            mock_success_get_routes_empty_response,
            mock_success_get_posts_empty_response,
            mock_success_create_route,
            mock_success_create_post
    ):
        response = client.post(
            f"{BASE_ROUTE}/posts", json=BASIC_PAYLOAD,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 201

        response_body = response.json()
        assert "data" in response_body
        assert "msg" in response_body

        assert response_body["data"]["id"] != ""
        assert response_body["data"]["id"] is not None
        assert response_body["data"]["userId"] == "ab99beb5-37e7-4e85-87e2-3578f92d883c"
        assert response_body["data"]["createdAt"] == "2023-10-05T21:20:53.214Z"
        assert response_body["data"]["expireAt"] == "2023-10-10T21:20:53.214Z"
        assert response_body["data"]["route"]["id"] == "a8ae58c4-1d41-4d3c-a3f8-f941906779b4"
        assert response_body["data"]["route"]["createdAt"] == "2023-09-25T21:20:54.214Z"


def test_rf003_get_route_failed_get_posts(
        client: TestClient
):
    """Checks that POST /rf003 fails when the user has a post in the system and the route is in the system"""

    with HTTMock(
            mock_success_auth,
            mock_success_get_routes,
            mock_success_get_posts
    ):
        response = client.post(
            f"{BASE_ROUTE}/posts", json=BASIC_PAYLOAD,
            headers={"Authorization": BASE_AUTH_TOKEN})
        assert response.status_code == 412
        response_body = response.json()
        assert "msg" in response_body
        assert response_body["msg"] == "El usuario ya tiene una publicación para la misma fecha"
