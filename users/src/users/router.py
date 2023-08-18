""" /users router """
import datetime
import json
import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
from psycopg2 import DataError
from pydantic import ValidationError
from sqlalchemy import delete, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src import database
from src.constants import datetime_to_str
from src.exceptions import UniqueConstraintViolatedException
from src.models import User
from src.users.schemas import CreateUserRequestSchema, CreateUserResponseSchema, UpdateUserRequestSchema
from src.users.utils import Users
from src.database import get_session

router = APIRouter()


@router.post("/")
def create_user(
        user_data: CreateUserRequestSchema, response: Response,
        sess: Annotated[Session, Depends(get_session)],
) -> CreateUserResponseSchema:
    """
    Creates a user with the given data.
    Username and email must be unique, validated by DB model UNIQUE constraint
    """
    try:
        users_util = Users()
        new_user = users_util.create_user(user_data, sess)
        response_body: CreateUserResponseSchema = CreateUserResponseSchema(
            id=str(new_user.id),
            createdAt=datetime_to_str(new_user.createdAt),
        )
        response.status_code = 201
        return response_body
    except UniqueConstraintViolatedException as e:
        print(e)
        raise HTTPException(status_code=412, detail="That email or username already exists")


@router.patch("/{user_id}")
def update_user(
        user_id: str, user_data: UpdateUserRequestSchema, response: Response,
        sess: Annotated[Session, Depends(get_session)],
) -> dict:
    """
    Updates a user with the given data.

    """
    try:
        retrieved_user = sess.execute(
            select(User).where(User.id == user_id)
        ).scalar_one()

        updated = False
        for field in ['status', 'dni', 'fullName', 'phoneNumber']:
            if getattr(user_data, field):
                setattr(retrieved_user, field, getattr(user_data, field))
                updated = True
        if updated:
            retrieved_user.updatedAt = datetime.datetime.now()
            sess.commit()
        else:
            raise HTTPException(status_code=400, detail="Solicitud vacía")
        return {"msg": "el usuario ha sido actualizado"}
    except (NoResultFound, DataError, TypeError):
        raise HTTPException(status_code=404, detail="El usuario no fue encontrado")


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
    Clears the users table
    Returns:
        msg: Todos los datos fueron eliminados
    """
    try:
        statement = delete(User)
        print(statement)
        with session:
            session.execute(statement)
            session.commit()
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=500, content={
                "msg": "Un error desconocido ha ocurrido", "error": json.dumps(e)
            })

    return {"msg": "Todos los datos fueron eliminados"}
