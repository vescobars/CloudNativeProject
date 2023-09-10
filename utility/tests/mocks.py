from httmock import HTTMock, all_requests

@all_requests
def mock_success_auth(url, request):
  return { 'status_code': 200 }

@all_requests
def mock_failed_auth(url, request):
  return { 'status_code': 401 }

@all_requests
def mock_forbidden_auth(url, request):
  return { 'status_code': 403 }