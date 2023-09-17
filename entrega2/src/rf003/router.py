from fastapi import APIRouter, HTTPException, Response, Request

from src.exceptions import UnauthorizedUserException, RouteNotFoundException, SuccessfullyDeletedRouteException, \
    ResponseException
from src.rf003.schemas import CreateRoutePostRequestSchema, CreatedRouteSchema
from src.rf003.utils import RF003
from src.schemas import RouteSchema, CreateRoutePostResponseSchema, CreatedPostSchema
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
                response: Response) -> CreateRoutePostResponseSchema:
    """
    Creates a post with the given data.
    """
    user_id, full_token = authenticate(request)
    route_id = None
    try:
        try:
            route: RouteSchema = CommonUtils.search_route(route_data.flightId, full_token)
        except RouteNotFoundException:
            route: CreatedRouteSchema = CommonUtils.create_route(route_data.flightId,
                                                                 route_data.sourceAirportCode,
                                                                 route_data.sourceCountry,
                                                                 route_data.destinyAirportCode,
                                                                 route_data.destinyCountry,
                                                                 route_data.bagCost,
                                                                 route_data.plannedStartDate,
                                                                 route_data.plannedEndDate,
                                                                 full_token)
        route_id = route.id
        RF003.validate_same_user_or_dates(route, route_data.expireAt)
        posts = RF003.get_post_filtered(None, route.id, user_id, full_token)
        if len(posts) == 0:
            post: CreatedPostSchema = CommonUtils.create_post(route.id, route_data.expireAt, full_token)
            final_response = CreateRoutePostResponseSchema(
                data=post,
                msg=f"Post (id={str(post.id)}) has been successfully created")
            response.status_code = 201
            return final_response
        else:
            RF003.validate_post(posts)
            post: CreatedPostSchema = CreatedPostSchema.model_validate(posts[0])
            final_response: CreateRoutePostResponseSchema = CreateRoutePostResponseSchema(
                data=post,
                msg="There is already a post in this route with your user")
            response.status_code = 201
            return final_response
    except ResponseException:
        RF003.delete_route(route_id, full_token)
        raise SuccessfullyDeletedRouteException()


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
