""" Router for routes microservice on /routes"""

import logging
from typing import Annotated

from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.requests import Request
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.constants import datetime_to_str
from src.database import get_session
from src.exception import UniqueConstraintViolatedException
from src.models import Route
from src.routes.schemas import CreateRouteRequestSchema, CreateRouteResponseSchema, GetRouteResponseSchema
from src.routes.utils import Routes

router = APIRouter()


@router.get("/")
async def see_and_filter_routes(
        sess: Annotated[Session, Depends(get_session)],
        response: Response,
        flight: Union[str, None] = None
):
    """
    Returns filtered routes
    :param response:
    :param flight:
    :param sess:
    """
    # TODO: Pending Auth (Implemented after finishing service and testing, before integration)
    if flight:
        filter_flightId = flight
        filtered_list = Routes.filter_flight_id(filter_flightId, sess)
        response.status_code = 200
        return filtered_list
    else:
        all_routes = Routes.get_all_routes(sess)
        response.status_code = 200
        return all_routes



@router.get("/ping")
async def ping():
    """
    Returns a pong when the endpoint is contacted.
    Essentially serves as a health check
    :return: pong text object with 200 status code
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


@router.post("/")
async def create_route(
        route_data: CreateRouteRequestSchema,
        request: Request,
        response: Response,
        sess: Annotated[Session, Depends(get_session)],
) -> CreateRouteResponseSchema:
    try:
        Routes.validate_token(request)

        routes_util = Routes()

        # Validates all required fields are present
        if not routes_util.validate_required_fields_create(route_data, sess):
            raise HTTPException(status_code=400)

        # Checks if the flightId already exists
        if routes_util.route_exists_flightid(route_data.flightId, sess):
            raise HTTPException(status_code=412)

        # Check if the dates are valid (in the past or not consecutive)
        if not routes_util.validate_dates(route_data.plannedStartDate, route_data.plannedEndDate):
            err_msg = {"msg": "Las fechas del trayecto no son válidas"}
            raise HTTPException(status_code=412, detail=err_msg)

        new_route = routes_util.create_routes(route_data, sess)

        # Route created successfully
        response_body: CreateRouteResponseSchema = CreateRouteResponseSchema(
            id=str(new_route.id),
            createdAt=datetime_to_str(new_route.createdAt),
        )

        response.status_code = 201
        return response_body

    except UniqueConstraintViolatedException as e:
        logging.error(e)
        err_msg = {"msg": "Un error desconocido ha ocurrido", "error": str(e)}
        raise HTTPException(status_code=500, detail=err_msg)


@router.get("/{route_id}")
async def get_route(
        route_id: str,
        response: Response,
        sess: Annotated[Session, Depends(get_session)],
):
    """
    Retrieves the route with the specified id
    :param sess:
    :param response:
    :param route_id: the route id
    :return:
    """
    # TODO: Pending Auth (Implemented after finishing service and testing, before integration)
    routes_util = Routes()

    # Validates route_id has an uuid4 format
    if not routes_util.id_is_uuid(route_id):
        raise HTTPException(status_code=400)

    # Go search for the route
    retrieved_route = Routes.get_route_id(route_id, sess)

    # Validates a route was found matching the id
    if retrieved_route is None:
        raise HTTPException(status_code=404)

    # Change response status code to 200 OK
    response.status_code = 200

    # Return the route in Route Schema
    return GetRouteResponseSchema(
        id=retrieved_route.id,
        flightId=retrieved_route.flightId,
        sourceAirportCode=retrieved_route.sourceAirportCode,
        sourceCountry=retrieved_route.sourceCountry,
        destinyAirportCode=retrieved_route.destinyAirportCode,
        destinyCountry=retrieved_route.destinyCountry,
        bagCost=retrieved_route.bagCost,
        plannedStartDate=retrieved_route.plannedStartDate,
        plannedEndDate=retrieved_route.plannedEndDate
    )


@router.delete("/{route_id}")
async def delete_route(
        route_id: str,
        response: Response,
        sess: Annotated[Session, Depends(get_session)],
):
    """
    Deletes the route with the specified id
    :param sess:
    :param response:
    :param route_id: the route id
    :return:
    """
    # TODO: Pending Auth (Implemented after finishing service and testing, before integration)
    routes_util = Routes()

    # Validates route_id has an uuid4 format
    if not routes_util.id_is_uuid(route_id):
        raise HTTPException(status_code=400)

    # Go search for the route
    retrieved_route = Routes.get_route_id(route_id, sess)

    # Validates a route was found matching the id
    if retrieved_route is None:
        raise HTTPException(status_code=404)

    # Deletes user
    Routes.delete_route_id(route_id, sess)

    # Change response status code to 200 OK
    response.status_code = 200

    # Returns message confirming the route was successfully deleted
    return {"msg": "Todos los datos fueron eliminados"}


