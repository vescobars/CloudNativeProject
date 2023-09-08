from .base_command import BaseCommannd
from ..models.route import Route, RouteSchema, CreatedRouteSchema
from ..session import Session
from ..errors.errors import IncompleteParams, FlightIdAlreadyExists, InvalidDates
from datetime import datetime, timedelta


class CreateRoute(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
            if not self.valid_dates():
                raise InvalidDates

            posted_route = RouteSchema(
                only=(
                    'flightId', 'sourceAirportCode', 'sourceCountry',
                    'destinyAirportCode', 'destinyCountry', 'bagCost',
                    'plannedStartDate', 'plannedEndDate'
                )
            ).load(self.data)
            route = Route(**posted_route)
            session = Session()

            if self.flight_id_exists(session):
                session.close()
                raise FlightIdAlreadyExists()

            session.add(route)
            session.commit()

            new_route = CreatedRouteSchema().dump(route)
            session.close()

            return new_route
        except (TypeError, KeyError):
            raise IncompleteParams()

    def flight_id_exists(self, session):
        existing_routes = session.query(Route).filter_by(
            flightId=self.data['flightId']
        ).all()

        return len(existing_routes) > 0
    
    def valid_dates(self):
        start_date = self.string_to_date(self.data['plannedStartDate'])
        end_date = self.string_to_date(self.data['plannedEndDate'])
        return start_date < end_date and not self.date_is_in_past(start_date)

    
    def date_is_in_past(self, date):
        current_utc_datetime = datetime.utcnow().date()
        return date < current_utc_datetime
    
    def string_to_date(self, date_string):
        # If last character is a Z remove it
        formatted_date = date_string[:-1] if date_string[-1] == 'Z' else date_string
        return datetime.fromisoformat(formatted_date).date()
