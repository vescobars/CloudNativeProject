""" Utils for routes"""
import datetime
import uuid
from time import timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session
from src.constants import now_utc
from src.exception import UniqueConstraintViolatedException

from src.models import Route
from src.schemas import RouteSchema
from src.routes.schemas import CreateRouteRequestSchema, CreateRouteResponseSchema


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
                    id=uuid.uuid4(),
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

                session.add(new_route)
                session.commit()
            except Exception as e:
                raise UniqueConstraintViolatedException()

        return new_route

    @staticmethod
    def id_is_uuid(id: str):
        """
        Confirms if a given id mathces the uuid 4 standard
        :param id:
        :return:True if the
        """
        try:
            uuid.UUID(id, version=4)  # Tries to cast the current id to uuid to see if its allowed
            return True
        except ValueError:
            return False

    @staticmethod
    def get_route_id(route_id: str, session: Session):
        """
        Searches for a route corresponding to the given id.
        Returns the route if it exists, else it returns none
        :param session: Current session
        :param route_id: the routes uuid
        :return: Route object if it exists, else None if no result was found
        """
        try:
            found_route = session.execute(
                select(Route).where(Route.id == route_id)
            ).scalar_one()
            return found_route
        except NoResultFound:
            return None

    @staticmethod
    def route_exists_flightid(flightid: str, session: Session):
        """
        Check if a route with the given flight_id exists in the database.
        :param flightid: Flight ID to check
        :param session: SQLAlchemy database session
        :return: True if the route exists, False otherwise
        """
        existing_route = session.execute(
            select(Route).where(Route.flightId == flightid)
        ).first()

        return existing_route is not None

    @staticmethod
    def validate_dates(planned_start_date: datetime, planned_end_date: datetime) -> bool:
        """
        Validate the planned dates of the route.
        :return: True if the dates are valid, False otherwise
        """
        # Assuming you have 'start_date' and 'end_date' attributes in your schema
        if not Route.plannedStartDate or not Route.plannedEndDate:
            return False  # Dates are missing, not valid

        # Check if start_date and end_date are in the past or not consecutive
        if planned_start_date < now_utc() or planned_end_date < now_utc():
            return False  # Date is not valid

        if planned_end_date < planned_start_date:
            return False

        return True  # Dates are valid

    @staticmethod
    def validate_required_fields_create(route_data: CreateRouteRequestSchema, session: Session) -> bool:
        """
        Validate if all the required fields are filled in for a create request.
        :param route_data: The route data to validate
        :param session: The SQLAlchemy database session (if needed)
        :return: True if all the fields are included, False otherwise
        """
        required_fields = [
            "flightId",
            "sourceAirportCode",
            "sourceCountry",
            "destinyAirportCode",
            "destinyCountry",
            "bagCost",
            "plannedStartDate",
            "plannedEndDate",
        ]

        for field_name in required_fields:
            if not hasattr(route_data, field_name) or getattr(route_data, field_name) is None:
                return False  # A required field is missing or has a None value

        return True  # All required fields are present and not None
