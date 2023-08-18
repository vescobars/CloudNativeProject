""" /users router """
import json
import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import delete
from sqlalchemy.orm import Session

from src import database
from src.constants import datetime_to_str
from src.exceptions import UniqueConstraintViolatedException
from src.models import User
from src.users.schemas import CreateUserRequestSchema, CreateUserResponseSchema
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
