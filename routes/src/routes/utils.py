""" Utils for routes"""
import datetime
from time import timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session

from src.models import Route
from src.schemas import RouteSchema
from src.routes.schemas import CreateRouteRequestSchema


class Routes:

    @staticmethod
    def create_routes(
            data: CreateRouteRequestSchema,
            session: Session
    ) -> RouteSchema:
        """
        Insert a new route into the Routes table in the db
        :param data:
        :param session:
        :return:
        """
        new_route = None
        with session:
            current_time = datetime.now(timezone.utc)
            try:
                new_route = Route(
                    flightId=data.flightId,
                    sourceAirportCode=data.sourceAirportCode,
                    sourceCountry=data.sourceCountry,
                    destinyAirportCode=data.destinyAirportCode,
                    destinyCountry=data.destinyCountry,
                    bagCost=data.bagCost,
                    plannedStartDate=data.plannedStartDate,
                    plannedEndDate=data.plannedEndDate,
                    createdAt=current_time,
                    updateAt=current_time,
                )
            except Exception as e:
                pass
                # Write specific exceptions

        return new_route
