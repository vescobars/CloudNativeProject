""" Router for users microservice on /routes"""

from fastapi import APIRouter, Response, Depends
from starlette.responses import JSONResponse

from sqlalchemy import delete
from sqlalchemy.orm import Session

import logging
from typing import Annotated, Union

from src.constants import datetime_to_str
from src.routes.schemas import CreateRouteRequestSchema, CreateRouteResponseSchema
from src.models import Route
from src.routes.utils import Routes
from src.database import get_session

router = APIRouter()


@router.post("/")
async def create_route(
        route_data: CreateRouteRequestSchema,
        response: Response,
        sess: Annotated[Session, Depends(get_session)],
) -> CreateRouteResponseSchema:
    """
    Creates a route with the given data.
    Planned dates must be older than the current date.
    Bag cost must be greater than zero, validated by pydantic
    :param route_data: route data with all specified params
    :param response: validated route request schema
    :param sess: current session
    :return: route response schema
    """
    try:
        routes_util = Routes()
        new_route = routes_util.create_routes(route_data, sess)
        response_body: CreateRouteResponseSchema = CreateRouteResponseSchema(
            id=str(new_route.id),
            createdAt=datetime_to_str(new_route.createdAt),
        )
        response.status_code = 201
        return response_body
    except Exception as e:
        logging.error(e)
        err_msg = {"msg": "Un error desconocido ha ocurrido", "error": str(e)}
        return JSONResponse(content=err_msg, status_code=500)


@router.get("/ping")
async def ping():
    """
    Returns a pong when the endpoint is contacted.
    Essentially serves as a health check
    :return: pong text object with 500 status code
    """
    return Response(content="pong", media_type="application/text", status_code=200)


@router.post("/reset")
async def reset(sess: Session = Depends(get_session)):
    """
    Clears route table in the db.
    :param sess: gets the current session
    :return: json -> msg: Todos los datos fueron eliminados
    """
    try:
        statement = delete(Route)
        with sess:
            sess.execute(statement)
            sess.commit()
    except Exception as e:
        logging.error(e)
        err_msg = {"msg": "Un error desconocido ha ocurrido", "error": str(e)}
        return JSONResponse(content=err_msg, status_code=500)
    return {"msg": "Todos los datos fueron eliminados"}
