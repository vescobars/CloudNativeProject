""" /users router """
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from sqlalchemy import delete

from src.database import engine
from src.models import User

router = APIRouter()


@router.post("/users")
async def create_user():
    """
    Creates a user with the given data.
    Username and email must be unique, validated by DB model UNIQUE constraint
    """

    return Response(content="pong", media_type="application/text", status_code=200)


@router.get("/ping")
async def ping():
    """
    Returns "pong" whenever the endpoint is contacted.
    Functions as a health check
    """
    return Response(content="pong", media_type="application/text", status_code=200)


@router.post("/reset")
async def reset():
    """
    Clears the users table
    Returns:
        msg: Todos los datos fueron eliminados
    """
    try:
        statement = delete(User)
        print(statement)
        with engine.connect() as conn:
            _ = conn.execute(statement)
            conn.commit()
    except Exception as e:
        print("ERROR: /users/reset")
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "msg": "Un error desconocido ha ocurrido"
            })

    return {"msg": "Todos los datos fueron eliminados"}
