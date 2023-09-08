from httmock import HTTMock, all_requests, response
from tests.utils.constants import STATIC_FAKE_UUID

@all_requests
def mock_success_auth(url, request):
  return response(200, { 'id': STATIC_FAKE_UUID }, {}, None, 5, request)

@all_requests
def mock_failed_auth(url, request):
  return { 'status_code': 401 }

@all_requests
def mock_forbidden_auth(url, request):
  return { 'status_code': 403 }