from httmock import response, urlmatch


@urlmatch(path=r'/users/me')
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


@urlmatch(path=r'/users/me')
def mock_failed_auth(url, request):
    return response(401)


@urlmatch(path=r'/users/me')
def mock_forbidden_auth(url, request):
    return response(403)


@urlmatch(method='GET', path=r'/posts/.+')
def mock_success_get_post(url, request):
    return response(200, content={
        "createdAt": "2023-09-14T03:16:41.782282",
        "expireAt": "2028-09-21T03:16:41.672000",
        "id": "86864ea3-69ed-4fca-9158-44c15a1e61a9",
        "routeId": "c915e59f-2ecf-4058-8728-257c23665467",
        "userId": "007734f7-1b1f-47f4-93b5-14b06e5994b1"
    })


@urlmatch(method='GET', path=r'/routes/.+')
def mock_success_get_route(url, request):
    return response(200, content={
        "bagCost": 152.0,
        "createdAt": "2023-09-14T03:16:34.810977",
        "destinyAirportCode": "LGW",
        "destinyCountry": "Inglaterra",
        "flightId": "813",
        "id": "c915e59f-2ecf-4058-8728-257c23665467",
        "plannedEndDate": "2023-09-24T03:16:34.710000",
        "plannedStartDate": "2023-09-16T03:16:34.710000",
        "sourceAirportCode": "BOG",
        "sourceCountry": "Colombia"
    })


@urlmatch(method='GET', path=r'/posts/.+')
def mock_failed_get_post_not_found(url, request):
    return response(404, content={
        "msg": "Route does not exist"
    })


@urlmatch(method='POST', path=r'/offers/?')
def mock_success_post_offer(url, request):
    return response(201, content={
        "createdAt": "2023-09-14T03:16:47.553601",
        "id": "a8ae58c4-1d41-4d3c-a3f8-f941906779b4",
        "userId": "cdab3f90-f8d8-458c-8447-ac8764f8e471"
    })


@urlmatch(method='delete', path=r'/offers/.*')
def mock_success_delete_offer(url, request):
    return response(200, content={
        "msg": "la oferta fue eliminada"
    })


@urlmatch(method='POST', path=r'/utility/?')
def mock_success_create_utility(url, request):
    return response(201, content={
        "offer_id": "3d747856-5ddb-467e-b9f4-2c7e2ef19245",
        "utility": 390.0,
        "createdAt": "2023-09-14T03:19:58.002748",
        "updateAt": "2023-09-14T03:19:58.002748"
    })


@urlmatch(method='POST', path=r'/utility/?')
def mock_failed_create_utility(url, request):
    return response(412, content={
        "detail": "A utility for that offer_id already exists"
    })


@urlmatch(method='GET', path=r'/posts/.+')
def mock_success_get_post_same_user_as_owner(url, request):
    return response(200, content={
        "createdAt": "2023-09-14T03:16:41.782282",
        "expireAt": "2028-09-21T03:16:41.672000",
        "id": "86864ea3-69ed-4fca-9158-44c15a1e61a9",
        "routeId": "c915e59f-2ecf-4058-8728-257c23665467",
        "userId": "cdab3f90-f8d8-458c-8447-ac8764f8e471"
    })


"""
POST /routes
{
    "createdAt": "2023-09-14T03:16:34.810977",
    "id": "c915e59f-2ecf-4058-8728-257c23665467"
}

GET /routes/:id

{
    "bagCost": 152.0,
    "createdAt": "2023-09-14T03:16:34.810977",
    "destinyAirportCode": "LGW",
    "destinyCountry": "Inglaterra",
    "flightId": "813",
    "id": "c915e59f-2ecf-4058-8728-257c23665467",
    "plannedEndDate": "2023-09-24T03:16:34.710000",
    "plannedStartDate": "2023-09-16T03:16:34.710000",
    "sourceAirportCode": "BOG",
    "sourceCountry": "Colombia"
}

POST /posts

{
    "createdAt": "2023-09-14T03:16:41.782282",
    "id": "86864ea3-69ed-4fca-9158-44c15a1e61a9",
    "userId": "007734f7-1b1f-47f4-93b5-14b06e5994b1"
}

GET /posts/:id

{
    "createdAt": "2023-09-14T03:16:41.782282",
    "expireAt": "2023-09-21T03:16:41.672000",
    "id": "86864ea3-69ed-4fca-9158-44c15a1e61a9",
    "routeId": "c915e59f-2ecf-4058-8728-257c23665467",
    "userId": "007734f7-1b1f-47f4-93b5-14b06e5994b1"
}


POST /offers
{
    "createdAt": "2023-09-14T03:16:47.553601",
    "id": "a8ae58c4-1d41-4d3c-a3f8-f941906779b4",
    "userId": "007734f7-1b1f-47f4-93b5-14b06e5994b1"
}

GET /offers/:id
{
    "createdAt": "2023-09-14T03:16:47.553601",
    "description": "reiciendis natus impedit",
    "fragile": false,
    "id": "a8ae58c4-1d41-4d3c-a3f8-f941906779b4",
    "offer": 299.0,
    "postId": "86864ea3-69ed-4fca-9158-44c15a1e61a9",
    "size": "LARGE",
    "userId": "007734f7-1b1f-47f4-93b5-14b06e5994b1"
}

POST /utility
{
    "offer_id": "3d747856-5ddb-467e-b9f4-2c7e2ef19245",
    "utility": 390.0,
    "createdAt": "2023-09-14T03:19:58.002748",
    "updateAt": "2023-09-14T03:19:58.002748"
}
"""
