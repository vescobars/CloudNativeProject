""" Utils for routes"""
import datetime
from time import timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session
from src.constants import now_utc

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
            current_time = now_utc()
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

    @staticmethod
    def route_exists(flight_id: str, session: Session) -> bool:
        """
        Check if a route with the given flight_id exists in the database.
        :param flight_id: Flight ID to check
        :param session: SQLAlchemy database session
        :return: True if the route exists, False otherwise
        """
        existing_route = session.execute(
            select(Route).where(Route.flight_id == flight_id)
        ).first()[0]

        return existing_route is None

    @staticmethod
    def validate_dates() -> bool:
        """
        Validate the planned dates of the route.
        :return: True if the dates are valid, False otherwise
        """
        # Assuming you have 'start_date' and 'end_date' attributes in your schema
        if not Route.plannedStartDate or not Route.plannedEndDate:
            return False  # Dates are missing, not valid

        current_date = now_utc()

        # Check if start_date and end_date are in the past or not consecutive
        if Route.plannedStartDate < now_utc() or Route.plannedStartDate < now_utc() or Route.plannedEndDate > Route.plannedStartDate:
            return False  # Dates are not valid

        return True  # Dates are valid
