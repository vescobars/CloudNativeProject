""" /users router """
import json
import logging
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from sqlalchemy.orm import Session
from typing import Annotated

from src.database import get_session
from src.exceptions import UniqueConstraintViolatedException, InvalidRequestException, \
    UtilityNotFoundException, UnauthorizedUserException
from src.models import Utility
from src.rf004.schemas import CreateOfferRequestSchema, CreateOfferResponseSchema
from src.rf004.utils import RF004
from src.schemas import UtilitySchema

router = APIRouter()


@router.get("/ping")
def ping():
    """
    Returns "pong" whenever the endpoint is contacted.
    Functions as a health check
    """
    return Response(content="pong", media_type="application/text", status_code=200)


"""
Como usuario deseo ofertar sobre alguna publicación de otro usuario para poder contratar un servicio.
    [ ]    El usuario brinda la información de la oferta que desea hacer y el identificador de la publicación a la que 
           se realiza.
    [ ]    Se valida que la publicación existe, solo se puede crear una oferta en una publicación existente.
    [ ]    Solo es posible crear la oferta si la publicación no ha expirado.
    [ ]    La oferta queda asociada al usuario de la sesión.
    [ ]    El usuario no debe poder ofertar en sus publicaciones.
    [ ]    Se calcula la utilidad (score) de la oferta.
    [X]    Solo un usuario autenticado puede realizar esta operación.
    [ ]    En cualquier caso de error la información al finalizar debe ser consistente.

"""


@router.post("/posts/{post_id}/offers")
def create_offer(
        offer_data: CreateOfferRequestSchema, post_id: str, request: Request, response: Response,
        sess: Annotated[Session, Depends(get_session)],
) -> CreateOfferResponseSchema:
    """
    Creates an offer with the given data.
    post_id must be linked to a valid post
    """
    user_id, full_token = authenticate(request)
    try:
        """
        get post and route
            in get post, validate expiration and check user id doesnt match
        create utility
        create offer (if it fails, delete utility)
        
        """
        rf004 = RF004(request.app.requests_client)

        new_user = Utilities().create_utility(util_data, sess)
        response.status_code = 201
        return new_user
    except UniqueConstraintViolatedException as e:
        print(e)
        raise HTTPException(status_code=412, detail="A utility for that offer_id already exists")


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
            user_id = RF004.authenticate_user(bearer_token)
        except UnauthorizedUserException:
            raise HTTPException(status_code=403, detail="Unauthorized. Valid credentials were rejected.")

    else:
        raise HTTPException(status_code=401, detail="No valid credentials were provided.")
    return user_id, full_token
