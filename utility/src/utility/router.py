""" /users router """
import json
import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.constants import datetime_to_str
from src.database import get_session
from src.exceptions import UniqueConstraintViolatedException, UserNotFoundException, InvalidRequestException, \
    IncorrectUserPasswordException, InvalidTokenException, ExpiredTokenException
from src.models import Utility
from src.utility.schemas import CreateUserRequestSchema, CreateUserResponseSchema, UpdateUserRequestSchema, \
    GenerateTokenRequestSchema, GenerateTokenResponseSchema, GetUserResponseSchema
from src.utility.utils import Utilities

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
        utility_util = Utilities()
        new_user = utility_util.create_utility(user_data, sess)
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
        user_id: str, user_data: UpdateUserRequestSchema,
        sess: Annotated[Session, Depends(get_session)],
) -> dict:
    """
    Updates a user with the given data.

    """
    try:
        updated = Users.update_user(user_id, user_data, sess)
        if updated:
            return {"msg": "el usuario ha sido actualizado"}
        else:
            raise InvalidRequestException()

    except InvalidRequestException:
        raise HTTPException(status_code=400, detail="Solicitud vacía")
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="El usuario no fue encontrado")


@router.post("/auth")
def generate_new_token(
        req_data: GenerateTokenRequestSchema,
        sess: Annotated[Session, Depends(get_session)],
) -> GenerateTokenResponseSchema:
    """
    Generates new security token if correctly authenticated
    """
    try:
        token_info = Users.generate_new_token(req_data, sess)
        return token_info

    except (IncorrectUserPasswordException, UserNotFoundException):
        raise HTTPException(status_code=404, detail="El usuario y/o contraseña no fue encontrado")


@router.get("/me")
def get_user(
        request: Request,
        sess: Annotated[Session, Depends(get_session)],
) -> GetUserResponseSchema:
    """
    Retrieves user if correctly authenticated
    """
    try:
        if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
            raise HTTPException(status_code=403, detail="El token no esta en el encabezado")
        user_id = Users.authenticate(request.headers.get('Authorization').split(" ")[1], sess)
        user_data = Users.get_user(user_id, sess)
        return user_data

    except (InvalidTokenException, ExpiredTokenException):
        raise HTTPException(status_code=401, detail="El usuario y/o contraseña no fue encontrado")


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
        return JSONResponse(status_code=500, content={
            "msg": "Un error desconocido ha ocurrido", "error": json.dumps(e)})
    return {"msg": "Todos los datos fueron eliminados"}
