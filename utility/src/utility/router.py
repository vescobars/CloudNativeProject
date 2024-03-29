""" /users router """
import json
import logging
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy import delete
from sqlalchemy.orm import Session
from typing import Annotated, List

from src.database import get_session
from src.exceptions import UniqueConstraintViolatedException, InvalidRequestException, \
    UtilityNotFoundException, UnauthorizedUserException
from src.models import Utility
from src.schemas import UtilitySchema
from src.utility.schemas import CreateUtilityRequestSchema, UpdateUtilityRequestSchema
from src.utility.utils import Utilities

router = APIRouter()


@router.get("/ping")
def ping():
    """
    Returns "pong" whenever the endpoint is contacted.
    Functions as a health check
    """
    return Response(content="pong", media_type="application/text", status_code=200)


@router.post("/reset")
async def reset(
        session: Session = Depends(get_session),
):
    """
    Clears the utilities table
    Returns:
        msg: Todos los datos fueron eliminados
    """
    try:
        statement = delete(Utility)
        print(statement)
        with session:
            session.execute(statement)
            session.commit()
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=500, content={
            "msg": "Un error desconocido ha ocurrido", "error": json.dumps(e)})
    return {"msg": "Todos los datos fueron eliminados"}


@router.post("/")
def create_utility(
        util_data: CreateUtilityRequestSchema, request: Request, response: Response,
        sess: Annotated[Session, Depends(get_session)],
) -> UtilitySchema:
    """
    Creates a utility with the given data.
    Offer_id must be unique
    """
    authenticate(request)
    try:
        new_user = Utilities().create_utility(util_data, sess)
        response.status_code = 201
        return new_user
    except UniqueConstraintViolatedException as e:
        print(e)
        raise HTTPException(status_code=412, detail="A utility for that offer_id already exists")


@router.get("/{offer_id}")
def get_utility(
        offer_id: str,
        sess: Annotated[Session, Depends(get_session)],
        request: Request) -> UtilitySchema:
    """
    Retrieves a utility with the given offer id.
    """
    authenticate(request)

    try:
        return Utilities.get_utility(offer_id, sess)

    except UtilityNotFoundException:
        raise HTTPException(status_code=404, detail="La utilidad no fue encontrado")


@router.post("/list")
def get_utilities(
        offer_ids: List[UUID4],
        sess: Annotated[Session, Depends(get_session)],
        request: Request) -> List[UtilitySchema]:
    """
    Retrieves a list of utilitie with the given offer ids.
    """
    authenticate(request)

    return Utilities.get_utilities(offer_ids, sess)


@router.patch("/{offer_id}")
def update_utility(
        offer_id: str, util_data: UpdateUtilityRequestSchema,
        sess: Annotated[Session, Depends(get_session)],
        request: Request) -> dict:
    """
    Updates a utility with the given data.

    """
    authenticate(request)

    try:
        updated = Utilities.update_utility(offer_id, util_data, sess)
        if updated:
            return {"msg": "la utilidad ha sido actualizada"}
        else:
            raise InvalidRequestException()

    except InvalidRequestException:
        raise HTTPException(status_code=400, detail="Solicitud invalida")
    except UtilityNotFoundException:
        raise HTTPException(status_code=404, detail="La utilidad no fue encontrado")


@router.delete("/{offer_id}")
def delete_utility(
        offer_id: str,
        sess: Annotated[Session, Depends(get_session)],
        request: Request) -> dict:
    """
    Deletes a utility with the given offer id.
    """
    authenticate(request)

    return {
        "deleted_offer_id": Utilities.delete_utility(offer_id, sess)
    }


def authenticate(request: Request) -> str:
    """
    Checks if authorization token is present and valid, then calls users endpoint to
    verify whether credentials are still authorized
    """
    if 'Authorization' in request.headers and 'Bearer ' in request.headers.get('Authorization'):
        bearer_token = request.headers.get('Authorization').split(" ")[1]
        try:
            user_id = Utilities.authenticate_user(bearer_token)
        except UnauthorizedUserException:
            raise HTTPException(status_code=401, detail="Unauthorized. Valid credentials were rejected.")

    else:
        raise HTTPException(status_code=403, detail="No valid credentials were provided.")
    return user_id
