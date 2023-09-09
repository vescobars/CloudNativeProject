""" /users router """
import json
import logging
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from sqlalchemy.orm import Session
from typing import Annotated

from src.database import get_session
from src.exceptions import UniqueConstraintViolatedException, InvalidRequestException, \
    UtilityNotFoundException
from src.models import Utility
from src.schemas import UtilitySchema
from src.utility.schemas import CreateUtilityRequestSchema, UpdateUtilityRequestSchema
from src.utility.utils import Utilities

router = APIRouter()


@router.post("/")
def create_utility(
        util_data: CreateUtilityRequestSchema, response: Response,
        sess: Annotated[Session, Depends(get_session)],
) -> UtilitySchema:
    """
    Creates a utility with the given data.
    Offer_id must be unique
    """
    try:
        new_user = Utilities().create_utility(str(util_data.offer_id), util_data.utility, sess)
        response.status_code = 201
        return new_user
    except UniqueConstraintViolatedException as e:
        print(e)
        raise HTTPException(status_code=412, detail="A utility for that offer_id already exists")


@router.patch("/{offer_id}")
def update_user(
        offer_id: str, util_data: UpdateUtilityRequestSchema,
        sess: Annotated[Session, Depends(get_session)],
) -> dict:
    """
    Updates a utility with the given data.

    """
    try:
        updated = Utilities.update_utility(offer_id, util_data.utility, sess)
        if updated:
            return {"msg": "la utilidad ha sido actualizada"}
        else:
            raise InvalidRequestException()

    except InvalidRequestException:
        raise HTTPException(status_code=400, detail="Solicitud invalida")
    except UtilityNotFoundException:
        raise HTTPException(status_code=404, detail="La utilidad no fue encontrado")


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
