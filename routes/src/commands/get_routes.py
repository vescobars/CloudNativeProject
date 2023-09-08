from .base_command import BaseCommannd
from ..models.route import Route, RouteSchema
from ..session import Session
from datetime import datetime, timedelta
from ..errors.errors import InvalidParams


class GetRoutes(BaseCommannd):
    def __init__(self, data):
        self.flight = data['flight'] if 'flight' in data else None

    def execute(self):
        session = Session()
        routes = session.query(Route).all()

        if self.flight != None:
            routes = [route for route in routes if route.flightId == self.flight]

        routes = RouteSchema(many=True).dump(routes)
        session.close()
        return routes
