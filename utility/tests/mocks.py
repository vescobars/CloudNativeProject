from httmock import all_requests, response


@all_requests
def mock_success_auth(url, request):
    return response(200, content={
        "id": "cdab3f90-f8d8-458c-8447-ac8764f8e471",
        "username": "test",
        "email": "test@gmail.com",
        "fullName": "Tester Person",
        "dni": "123456789",
        "phoneNumber": "+57 123456789",
        "status": "VERIFICADO"
    })


@all_requests
def mock_failed_auth(url, request):
    return response(401)


@all_requests
def mock_forbidden_auth(url, request):
    return response(403)
