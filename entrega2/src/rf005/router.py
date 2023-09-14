""" /users router """

from fastapi import APIRouter, HTTPException, Response, Request

from src.exceptions import UnauthorizedUserException
from src.rf004.schemas import CreateOfferResponseSchema
from src.rf005.utils import RF005
from src.schemas import PostSchema, RouteSchema, CreatedOfferSchema
from src.utils import CommonUtils

router = APIRouter()


@router.get("/ping")
def ping():
    """
    Returns "pong" whenever the endpoint is contacted.
    Functions as a health check
    """
    return Response(content="pong", media_type="application/text", status_code=200)


@router.get("/posts/{post_id}")
def find_post(
        post_id: str, request: Request, response: Response,
) -> CreateOfferResponseSchema:
    """
    Returns info about a specific post, its route, and all its offers sorted according to utility
    """
    user_id, full_token = authenticate(request)

    post: PostSchema = CommonUtils.get_post(post_id, user_id, full_token)
    route: RouteSchema = CommonUtils.get_route(post.routeId, full_token)

    # TODO create methods to get list of offers

    offers = RF005.get_filtered_offers(post.id, full_token)

    returned_offer = CreatedOfferSchema(
        id=offer.id,
        userId=offer.userId,
        createdAt=offer.createdAt,
        postId=post.id
    )
    final_response = CreateOfferResponseSchema(
        data=returned_offer,
        msg=f"Offer (id={str(offer.id)}) has been successfully created")

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
