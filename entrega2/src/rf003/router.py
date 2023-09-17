from fastapi import APIRouter, HTTPException, Response, Request

from src.exceptions import UnauthorizedUserException, RouteNotFoundException, SuccessfullyDeletedRouteException, \
    ResponseException
from src.rf003.schemas import CreateRoutePostRequestSchema, CreatedRouteSchema, CreatePostResponseSchema, \
    PostWithRouteSchema, CreatedPostSchema
from src.rf003.utils import RF003
from src.schemas import RouteSchema
from src.utils import CommonUtils

router = APIRouter()


@router.get("/ping")
def ping():
    """
    Returns "pong" whenever the endpoint is contacted.
    Functions as a health check
    """
    return Response(content="pong", media_type="application/text", status_code=200)


@router.post("/posts")
def create_post(route_data: CreateRoutePostRequestSchema, request: Request,
                response: Response) -> CreatePostResponseSchema:
    """
    Creates a post with the given data.
    """
    user_id, full_token = authenticate(request)
    route_created = False
    RF003.validate_same_user_or_dates(route_data.plannedStartDate, route_data.plannedEndDate, route_data.expireAt)
    try:
        route: RouteSchema = CommonUtils.search_route(route_data.flightId, full_token)
        RF003.validate_same_user_or_dates(route.plannedStartDate, route.plannedEndDate, route_data.expireAt)
    except RouteNotFoundException:
        created_route: CreatedRouteSchema = CommonUtils.create_route(
            route_data.flightId,
            route_data.origin.airportCode,
            route_data.origin.country,
            route_data.destiny.airportCode,
            route_data.destiny.country,
            route_data.bagCost,
            route_data.plannedStartDate,
            route_data.plannedEndDate,
            full_token)
        route: RouteSchema = RouteSchema(
            id=created_route.id,
            flightId=route_data.flightId,
            sourceAirportCode=route_data.origin.airportCode,
            sourceCountry=route_data.origin.country,
            destinyAirportCode=route_data.destiny.airportCode,
            destinyCountry=route_data.destiny.country,
            bagCost=route_data.bagCost,
            plannedStartDate=route_data.plannedStartDate,
            plannedEndDate=route_data.plannedEndDate,
            createdAt=created_route.createdAt)
        route_created = True

    posts = RF003.get_post_filtered(None, route.id, user_id, full_token)
    if len(posts) == 0:
        try:
            post_raw: CreatedPostSchema = CommonUtils.create_post(route.id, route_data.expireAt, full_token)
            post: PostWithRouteSchema = PostWithRouteSchema(
                **post_raw.model_dump(),
                route=CreatedRouteSchema(
                    id=route.id,
                    createdAt=route.createdAt
                ),
            )
            final_response = CreatePostResponseSchema(
                data=post,
                msg=f"Post (id={str(post.id)}) has been successfully created")
            response.status_code = 201
            return final_response
        except ResponseException as e:
            print(e)
            if route_created:
                RF003.delete_route(route.id, full_token)
                raise SuccessfullyDeletedRouteException()

    else:
        RF003.validate_post(posts)
        post: PostWithRouteSchema = PostWithRouteSchema(
            route=CreatedRouteSchema(
                id=route.id,
                createdAt=route.createdAt
            ),
            id=posts[0].id,
            userId=posts[0].userId,
            createdAt=posts[0].createdAt,
            expireAt=posts[0].expireAt)
        final_response: CreatePostResponseSchema = CreatePostResponseSchema(
            data=post,
            msg="There is already a post in this route with your user")
        response.status_code = 201
        return final_response


def authenticate(request: Request) -> tuple[str, str]:
    """
    Checks if authorization token is present and valid, then calls users endpoint to
    verify whether credentials are still authorized

    Returns the user's id, and the full bearer token present in the
        authentication header (including the "Bearer " prefix)
    """
    if 'Authorization' in request.headers and 'Bearer ' in request.headers.get('Authorization'):
        full_token = request.headers.get('Authorization')
        bearer_token = full_token.split(" ")[1]
        try:
            user_id = CommonUtils.authenticate_user(bearer_token)
        except UnauthorizedUserException:
            raise HTTPException(status_code=401, detail="Unauthorized. Valid credentials were rejected.")

    else:
        raise HTTPException(status_code=403, detail="No valid credentials were provided.")
    return user_id, full_token
