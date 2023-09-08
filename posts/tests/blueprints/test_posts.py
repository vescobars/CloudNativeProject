from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.models.post import Post
from src.errors.errors import ApiError
from datetime import datetime, timedelta
from tests.mocks import mock_failed_auth, mock_success_auth, mock_forbidden_auth
from httmock import HTTMock
from uuid import uuid4
from src.main import app
import json
import uuid
from tests.utils.constants import STATIC_FAKE_UUID

class TestPosts():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_post(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/posts', json={
            'routeId': str(uuid.uuid4()),
            'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
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
  
  def test_create_post_without_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.post(
          '/posts', json={
            'routeId': str(uuid.uuid4()),
            'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
          }
        )
        assert response.status_code == 403

  def test_create_post_invalid_token(self):
    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.post(
          '/posts', json={
            'routeId': str(uuid.uuid4()),
            'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_create_post_invalid_dates(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.post(
          '/posts', json={
            'routeId': str(uuid.uuid4()),
            'expireAt': (datetime.now() - timedelta(days=2)).isoformat()
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 412

  def test_get_post(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    post = CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/posts/{post["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in response_json
        assert 'routeId' in response_json
        assert 'userId' in response_json
        assert 'expireAt' in response_json
  
  def test_get_post_without_token(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    post = CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.get(
          f'/posts/{post["id"]}'
        )
        assert response.status_code == 403

  def test_get_post_invalid_token(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    post = CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/posts/{post["id"]}',
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_get_post_invalid_id(self):
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/posts/invalid',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 400

  def test_get_post_doesnt_exist(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    post = CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/posts/{STATIC_FAKE_UUID}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 404

  def test_get_posts(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = STATIC_FAKE_UUID
    CreatePost(data, userId).execute()
    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.get(
          f'/posts',
          query_string={
            'route': data['routeId'],
            'expire': 'false',
            'owner': 'me'
          },
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)
        assert response.status_code == 200
        assert len(response_json) == 1
        assert 'id' in response_json[0]
        assert 'routeId' in response_json[0]
        assert 'userId' in response_json[0]
        assert 'expireAt' in response_json[0]

  def test_get_posts_without_token(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.get(
          f'/posts',
          query_string={
            'route': data['routeId'],
            'expire': 'false',
            'owner': 'me'
          }
        )
        assert response.status_code == 403

  def test_get_posts_invalid_token(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.get(
          f'/posts',
          query_string={
            'route': data['routeId'],
            'expire': 'false',
            'owner': 'me'
          },
          headers={
            'Authorization': f'Bearer Invalid'
          }
        )
        assert response.status_code == 401

  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get(
        '/posts/ping'
      )
      assert response.status_code == 200
      assert response.data.decode("utf-8") == 'pong'

  def test_delete_route(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    post = CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_success_auth):
        response = test_client.delete(
          f'/posts/{post["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        response_json = json.loads(response.data)

        assert response.status_code == 200
        assert 'msg' in response_json

  def test_delete_route_invalid_token(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    post = CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_failed_auth):
        response = test_client.delete(
          f'/posts/{post["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 401

  def test_delete_route_without_token(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    post = CreatePost(data, userId).execute()

    with app.test_client() as test_client:
      with HTTMock(mock_forbidden_auth):
        response = test_client.delete(
          f'/posts/{post["id"]}',
          headers={
            'Authorization': f'Bearer {uuid4()}'
          }
        )
        assert response.status_code == 403

  def test_reset(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/posts/reset'
      )
      assert response.status_code == 200

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)