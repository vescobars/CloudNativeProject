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


@urlmatch(method='GET', path=r'/offers/?')
def mock_success_search_offers(url, request):
    return response(200, content=[
        {
            "createdAt": "2023-09-14T08:23:33.177625",
            "description": "ea quod deleniti 1",
            "fragile": False,
            "id": "868544f6-6c86-489e-b68f-f6e2ec5ca857",
            "offer": 400,
            "postId": "68158796-9594-4b4f-a184-8df97379e912",
            "size": "MEDIUM",
            "userId": "d598228c-7516-4177-a9d7-e7f2bf842a4d"
        },
        {
            "createdAt": "2023-09-14T08:23:33.177625",
            "description": "ea quod deleniti 2",
            "fragile": False,
            "id": "3fa8eb34-5e79-4daf-aba7-84c007ff0445",
            "offer": 600,
            "postId": "68158796-9594-4b4f-a184-8df97379e912",
            "size": "MEDIUM",
            "userId": "06d0d441-bb2c-4c89-af01-99fa2cfc08a1"
        }, {
            "createdAt": "2023-09-14T08:23:33.177625",
            "description": "ea quod deleniti 3",
            "fragile": False,
            "id": "67b34f5b-31a5-4b0e-ae4e-bafac1a09aa9",
            "offer": 500,
            "postId": "68158796-9594-4b4f-a184-8df97379e912",
            "size": "MEDIUM",
            "userId": "f99c5544-7503-46d4-bc4e-c703bac72747"
        }, {
            "createdAt": "2023-09-14T08:23:33.177625",
            "description": "ea quod deleniti 4",
            "fragile": False,
            "id": "74670a89-9976-4562-813a-6ba48ae962da",
            "offer": 9000,
            "postId": "68158796-9594-4b4f-a184-8df97379e912",
            "size": "MEDIUM",
            "userId": "f99c5544-7503-46d4-bc4e-c703bac72747"
        }
    ])


@urlmatch(method='GET', path=r'/posts/.+')
def mock_success_get_post(url, request):
    return response(200, content={
        "createdAt": "2023-09-14T03:16:41.782282",
        "expireAt": "2028-09-21T03:16:41.672000",
        "id": "68158796-9594-4b4f-a184-8df97379e912",
        "routeId": "c915e59f-2ecf-4058-8728-257c23665467",
        "userId": "cdab3f90-f8d8-458c-8447-ac8764f8e471"
    })


@urlmatch(method='GET', path=r'/posts/.+')
def mock_success_get_post_different_owner(url, request):
    return response(200, content={
        "createdAt": "2023-09-14T03:16:41.782282",
        "expireAt": "2028-09-21T03:16:41.672000",
        "id": "68158796-9594-4b4f-a184-8df97379e912",
        "routeId": "c915e59f-2ecf-4058-8728-257c23665467",
        "userId": "89c3394d-3abe-431a-896e-c57fb90441a7"
    })


@urlmatch(method='GET', path=r'/routes/.+')
def mock_success_get_route(url, request):
    return response(200, content={
        "bagCost": 40,
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


@urlmatch(method='POST', path=r'/utility/list/?')
def mock_success_search_utilities(url, request):
    return response(200, content=[
        {
            "offer_id": "74670a89-9976-4562-813a-6ba48ae962da",
            "utility": 8980.0,
            "createdAt": "2023-09-14T08:14:42.116372",
            "updateAt": "2023-09-14T08:14:42.116372"
        },
        {
            "offer_id": "3fa8eb34-5e79-4daf-aba7-84c007ff0445",
            "utility": 580.0,
            "createdAt": "2023-09-14T08:14:48.465019",
            "updateAt": "2023-09-14T08:14:48.465019"
        },
        {
            "offer_id": "67b34f5b-31a5-4b0e-ae4e-bafac1a09aa9",
            "utility": 480.0,
            "createdAt": "2023-09-14T08:14:50.668479",
            "updateAt": "2023-09-14T08:14:50.668479"
        },
        {
            "offer_id": "868544f6-6c86-489e-b68f-f6e2ec5ca857",
            "utility": 380.0,
            "createdAt": "2023-09-14T08:14:42.116372",
            "updateAt": "2023-09-14T08:14:42.116372"
        }
    ])


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


@urlmatch(method='GET', path=r'/posts/.+')
def mock_success_get_post_expired(url, request):
    return response(200, content={
        "createdAt": "2023-09-14T03:16:41.742282",
        "expireAt": "2020-09-21T03:16:41.672000",
        "id": "86864ea3-69ed-4fca-9158-44c15a1e61a9",
        "routeId": "c915e59f-2ecf-4058-8728-257c23665467",
        "userId": "007734f7-1b1f-47f4-93b5-14b06e5994b1"
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
