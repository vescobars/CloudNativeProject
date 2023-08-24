""" Router for users microservice on /routes"""
from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse

import json

from requests import session

from src.routes.utils import Route
from sqlalchemy import delete
from sqlalchemy.orm import Session
from src.models import Route
from src.routes.utils import Route
from src.database import get_session

router = APIRouter()


@router.get("/ping")
async def ping():
    return Response(content="pong", media_type="application/text", status_code=200)


@router.post("/reset")
async def reset(
        session: Session = Depends(get_session)
):
    try:
        statement = delete(Route)
        with session:
            session.execute(statement)
            session.commit()
    except Exception as e:
        err_msg = {"msg": "Un error desconocido ha ocurrido", "error": json.dumps(e)}
        return JSONResponse(content=err_msg, status_code=500)
    return {"msg": "Todos los datos fueron eliminados"}