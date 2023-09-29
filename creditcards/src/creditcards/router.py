""" /users router """
import json
import logging
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.constants import datetime_to_str, SECRET_FAAS_TOKEN
from src.creditcards.schemas import CreateCCRequestSchema, CreateCCResponseSchema, UpdateCCStatusRequestSchema
from src.creditcards.utils import CreditCardUtils
from src.database import get_session
from src.exceptions import UnauthorizedUserException, InvalidRequestException
from src.models import CreditCard
from src.utils import CommonUtils

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
    Clears the credit card table
    Returns:
        msg: Todos los datos fueron eliminados
    """
    try:
        statement = delete(CreditCard)
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
def create_card(
        card_data: CreateCCRequestSchema, request: Request, response: Response,
        sess: Annotated[Session, Depends(get_session)],
) -> CreateCCResponseSchema:
    """
    Creates a credit card with the given data.
    """
    user_id, _ = authenticate(request)
    new_card_id, created_at = CreditCardUtils().create_card(card_data, user_id, sess)
    response.status_code = 201
    return CreateCCResponseSchema(
        id=new_card_id,
        userId=user_id,
        createdAt=datetime_to_str(created_at)
    )


@router.get("/")
def get_credit_cards(
        offer_ids: List[UUID4],
        sess: Annotated[Session, Depends(get_session)],
        request: Request) -> List[UtilitySchema]:
    """
    Retrieves a list of utilitie with the given offer ids.
    """
    user_id, _ = authenticate(request)

    return Utilities.get_utilities(offer_ids, sess)


@router.post("/{ruv}")
def update_card_state(
        data: UpdateCCStatusRequestSchema,
        sess: Annotated[Session, Depends(get_session)],
        request: Request) -> dict:
    """
    Updates a credit card status with the given data.
    :param data:
    :param sess:
    :param request:
    :return:
    """
    authenticate_secret_token(request)
    ruv = request.path_params.get("ruv")
    try:
        updated = CreditCardUtils.update_status(ruv, data, sess)
        if updated:
            return {"msg": "Credit card successfully updated"}
        else:
            raise InvalidRequestException()

    except InvalidRequestException:
        raise HTTPException(status_code=400, detail="Solicitud invalida")



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


def authenticate_secret_token(request: Request) -> None:
    """
    Checks if bearer token matches FaaS secret token
    """
    if 'Authorization' in request.headers and 'Bearer ' in request.headers.get('Authorization'):
        full_token = request.headers.get('Authorization')
        bearer_token = full_token.split(" ")[1]

        if bearer_token != SECRET_FAAS_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized. Valid credentials were rejected.")
    else:
        raise HTTPException(status_code=403, detail="No valid credentials were provided.")
