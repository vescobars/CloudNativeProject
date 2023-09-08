from src.commands.create_offer import CreateOffer
from src.session import Session, engine
from src.models.model import Base
from src.models.offer import Offer
from src.errors.errors import ApiError
from datetime import datetime, timedelta
from tests.mocks import mock_failed_auth, mock_success_auth, mock_forbidden_auth
from httmock import HTTMock
from src.main import app
from uuid import uuid4
import json
from tests.utils.constants import STATIC_FAKE_UUID

class TestOffers():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.userId = STATIC_FAKE_UUID

  def test_create_offer(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/offers', json={
            'postId': str(uuid4()),
            'description': 'My description',
            'size': 'LARGE',
            'fragile': True,
            'offer': 10
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 201
        assert 'id' in response_json
        assert 'userId' in response_json
        assert 'createdAt' in response_json

  def test_create_offer_invalid_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.post(
          '/offers', json={
            'postId': str(uuid4()),
            'description': 'My description',
            'size': 'LARGE',
            'fragile': True,
            'offer': 10
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_create_offer_without_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.post(
          '/offers', json={
            'postId': str(uuid4()),
            'description': 'My description',
            'size': 'LARGE',
            'fragile': True,
            'offer': 10
          }
        )
        assert response.status_code == 403

  def test_create_offer_missing_fields(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/offers', json={
            'postId': str(uuid4()),
            'offer': 10
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_create_offer_invalid_size(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/offers', json={
            'postId': str(uuid4()),
            'description': 'My description',
            'size': 'invalid',
            'fragile': True,
            'offer': 10
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 412

  def test_create_negative_offer(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/offers', json={
            'postId': str(uuid4()),
            'description': 'My description',
            'size': 'LARGE',
            'fragile': True,
            'offer': -10
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 412

  def test_get_offer(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    offer = CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/offers/{offer["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json
        assert 'postId' in response_json
        assert 'description' in response_json
        assert 'size' in response_json
        assert 'fragile' in response_json
        assert 'offer' in response_json
        assert 'createdAt' in response_json

  def test_get_offer_invalid_token(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    offer = CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/offers/{offer["id"]}',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_offer_without_token(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    offer = CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.get(
          f'/offers/{offer["id"]}'
        )
        assert response.status_code == 403

  def test_get_offer_invalid_id(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    offer = CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/offers/invalid',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_get_offer_doesnt_exist(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    offer = CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/offers/{STATIC_FAKE_UUID}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 404

  def test_get_offers(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/offers',
          query_string={
            'post': data['postId'],
            'filter': 'me'
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 1
        assert 'id' in response_json[0]
        assert 'postId' in response_json[0]
        assert 'description' in response_json[0]
        assert 'size' in response_json[0]
        assert 'fragile' in response_json[0]
        assert 'offer' in response_json[0]
        assert 'createdAt' in response_json[0]

  def test_get_offers_invalid_token(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/offers',
          query_string={
            'post': data['postId'],
            'filter': 'me'
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_offers_without_token(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.get(
          f'/offers',
          query_string={
            'post': data['postId'],
            'filter': 'me'
          }
        )
        assert response.status_code == 403

  def test_get_offers_invalid_post_id(self): 
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    CreateOffer(data, self.userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/offers',
          query_string={
            'post': 'invalid',
            'filter': 'me'
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_delete_route(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    userId = str(uuid4())
    offer = CreateOffer(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.delete(
          f'/offers/{offer["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)

        assert response.status_code == 200
        assert 'msg' in response_json

  def test_delete_route_invalid_token(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    userId = str(uuid4())
    offer = CreateOffer(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.delete(
          f'/offers/{offer["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 401

  def test_delete_route_without_token(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    userId = str(uuid4())
    offer = CreateOffer(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.delete(
          f'/offers/{offer["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 403



  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get(
        '/offers/ping'
      )
      assert response.status_code == 200
      assert response.data.decode("utf-8") == 'pong'

  def test_reset(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/offers/reset'
      )
      assert response.status_code == 200

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)