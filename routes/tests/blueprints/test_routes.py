from src.session import Session, engine
from src.models.model import Base
from src.models.route import Route
from src.main import app
import json
from uuid import uuid4
from src.commands.create_route import CreateRoute
from datetime import datetime, timedelta
from tests.mocks import mock_failed_auth, mock_success_auth, mock_forbidden_auth
from httmock import HTTMock
from tests.utils.constants import STATIC_FAKE_UUID

class TestRoutes():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_route(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/routes', json={
            'flightId': 'A2',
            'sourceAirportCode': 'LAX',
            'sourceCountry': 'USA',
            'destinyAirportCode': 'BOG',
            'destinyCountry': 'CO',
            'bagCost': 100,
            'plannedStartDate': datetime.utcnow().isoformat(),
            'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 201
        assert 'id' in response_json
        assert 'createdAt' in response_json
  
  def test_create_route_invalid_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.post(
          '/routes', json={
            'flightId': 'A2',
            'sourceAirportCode': 'LAX',
            'sourceCountry': 'USA',
            'destinyAirportCode': 'BOG',
            'destinyCountry': 'CO',
            'bagCost': 100,
            'plannedStartDate': datetime.utcnow().isoformat(),
            'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )

        assert response.status_code == 401

  def test_create_route_without_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.post(
          '/routes', json={
            'flightId': 'A2',
            'sourceAirportCode': 'LAX',
            'sourceCountry': 'USA',
            'destinyAirportCode': 'BOG',
            'destinyCountry': 'CO',
            'bagCost': 100,
            'plannedStartDate': datetime.utcnow().isoformat(),
            'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
          }
        )

        assert response.status_code == 403

  def test_create_route_missing_fields(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/routes', json={
            'bagCost': 100
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        assert response.status_code == 400

  def test_create_route_already_exist(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    CreateRoute(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/routes', json=data,
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        assert response.status_code == 412

  def test_get_routes(self):
    route_data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    CreateRoute(route_data).execute()
    data = {
      'flight': route_data['flightId']
    }

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          '/routes', query_string=data,
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 1
        assert 'id' in response_json[0]
        assert 'sourceAirportCode' in response_json[0]
        assert 'sourceCountry' in response_json[0]
        assert 'destinyAirportCode' in response_json[0]
        assert 'destinyCountry' in response_json[0]
        assert 'bagCost' in response_json[0]
        assert 'flightId' in response_json[0]
        assert 'plannedStartDate' in response_json[0]
        assert 'plannedEndDate' in response_json[0]

  def test_get_routes_invalid_token(self):
    route_data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    CreateRoute(route_data).execute()
    data = {
      'flight': route_data['flightId']
    }

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          '/routes', query_string=data,
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_routes_without_token(self):
    route_data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    CreateRoute(route_data).execute()
    data = {
      'flight': route_data['flightId']
    }

    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.get(
          '/routes', query_string=data
        )
        assert response.status_code == 403

  def test_get_route(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    route = CreateRoute(data).execute()
  
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/routes/{route["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json
        assert 'sourceAirportCode' in response_json
        assert 'sourceCountry' in response_json
        assert 'destinyAirportCode' in response_json
        assert 'destinyCountry' in response_json
        assert 'bagCost' in response_json
        assert 'flightId' in response_json
        assert 'plannedStartDate' in response_json
        assert 'plannedEndDate' in response_json

  def test_get_route_invalid_token(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    route = CreateRoute(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/routes/{route["id"]}',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )

        assert response.status_code == 401

  def test_get_route_without_token(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    route = CreateRoute(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.get(
          f'/routes/{route["id"]}'
        )

        assert response.status_code == 403

  def test_get_route_invalid_id(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/routes/invalid',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        assert response.status_code == 400

  def test_get_route_doesnt_exist(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    route = CreateRoute(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/routes/{STATIC_FAKE_UUID}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )

        assert response.status_code == 404

  def test_delete_route(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    route = CreateRoute(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.delete(
          f'/routes/{route["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)

        assert response.status_code == 200
        assert 'msg' in response_json

  def test_delete_route_invalid_token(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    route = CreateRoute(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.delete(
          f'/routes/{route["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 401

  def test_delete_route_without_token(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    route = CreateRoute(data).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.delete(
          f'/routes/{route["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 403

  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get(
        '/routes/ping'
      )
      assert response.status_code == 200
      assert response.data.decode("utf-8") == 'pong'

  def test_reset(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/routes/reset'
      )
      assert response.status_code == 200

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)