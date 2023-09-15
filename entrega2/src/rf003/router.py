import uuid

from fastapi import APIRouter, HTTPException, Response, Request
from src.rf003.schemas import CreateRoutePostRequestSchema, CreateRoutePostResponseSchema, CreatedRouteSchema
from src.rf003.utils import RF003
from src.schemas import RouteSchema
from src.utils import CommonUtils
from src.exceptions import UnauthorizedUserException, RouteNotFoundException

router = APIRouter()


@router.get("/ping")
def ping():
    """
    Returns "pong" whenever the endpoint is contacted.
    Functions as a health check
    """
    return Response(content="pong", media_type="application/text", status_code=200)


@router.post("/routes/{route_id}/posts")
def create_post(route_data: CreateRoutePostRequestSchema, route_id: str, request: Request,
                response: Response) -> CreateRoutePostResponseSchema:
    """
    Creates a post with the given data.
    """
    user_id, full_token = authenticate(request)
    try:
        route: RouteSchema = CommonUtils.get_route(uuid.UUID(route_id), full_token)
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

    return None


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
