from httmock import response, urlmatch


@urlmatch(path=r'/users/me')
def mock_success_auth(url, request):
    return response(200, content={
        "id": "ab99beb5-37e7-4e85-87e2-3578f92d883c",
        "username": "test",
        "email": "test@gmail.com",
        "fullName": "Tester Person",
        "dni": "123456789",
        "phoneNumber": "+57 123456789",
        "status": "VERIFICADO"
    })


@urlmatch(path=r'/users/me')
def mock_failed_auth(url, request):
    return response(401)


@urlmatch(path=r'/users/me')
def mock_forbidden_auth(url, request):
    return response(403)


@urlmatch(method='GET', path=r'/routes')
def mock_success_get_routes(url, request):
    return response(200, content=[{
        "id": "a8ae58c4-1d41-4d3c-a3f8-f941906779b4",
        "flightId": "abcdfghijklm",
        "sourceAirportCode": "KJFK",
        "sourceCountry": "USA",
        "destinyAirportCode": "KDFW",
        "destinyCountry": "USA",
        "bagCost": 100,
        "plannedStartDate": "2023-10-13T21:20:50.214Z",
        "plannedEndDate": "2023-10-14T21:20:54.214Z",
        "createdAt": "2023-09-25T21:20:54.214Z"
    }])


@urlmatch(method='GET', path=r'/routes')
def mock_success_get_routes_empty_response(url, request):
    return response(200, content=[])


@urlmatch(method='GET', path=r'/posts?')
def mock_success_get_posts(url, request):
    return response(200, content=[
        {
            "id": "0bf7c23b-ba49-48ff-8e38-2140d0307264",
            "routeId": "a8ae58c4-1d41-4d3c-a3f8-f941906779b4",
            "userId": "ab99beb5-37e7-4e85-87e2-3578f92d883c",
            "expireAt": "2023-10-10T21:20:53.214Z",
            "createdAt": "2023-10-05T21:20:54.214Z"
        }
    ])


@urlmatch(method='GET', path=r'/posts?')
def mock_success_get_posts_empty_response(url, request):
    return response(200, content=[])


@urlmatch(method='POST', path=r'/posts')
def mock_success_create_post(url, request):
    return response(201, content={
        "id": "0bf7c23b-ba49-48ff-8e38-2140d0307264",
        "userId": "ab99beb5-37e7-4e85-87e2-3578f92d883c",
        "createdAt": "2023-10-05T21:20:53.214Z",
        "expireAt": "2023-10-10T21:20:53.214Z"
    })


@urlmatch(method='POST', path=r'/posts')
def mock_failed_create_post(url, request):
    return response(400, content="Invalid Parameters")


@urlmatch(method='POST', path=r'/routes')
def mock_success_create_route(url, request):
    return response(201, content={
        "id": "a8ae58c4-1d41-4d3c-a3f8-f941906779b4",
        "createdAt": "2023-09-25T21:20:54.214Z"
    })
