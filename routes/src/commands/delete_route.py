from .base_command import BaseCommannd
from ..models.route import Route, RouteSchema
from ..session import Session
from ..errors.errors import InvalidParams, RouteNotFoundError


class DeleteRoute(BaseCommannd):
    def __init__(self, route_id):
        if self.is_uuid(route_id):
            self.route_id = route_id
        else:
            raise InvalidParams()

    def execute(self):
        session = Session()
        if len(session.query(Route).filter_by(id=self.route_id).all()) <= 0:
            session.close()
            raise RouteNotFoundError()

        route = session.query(Route).filter_by(id=self.route_id).one()
        session.delete(route)
        session.commit()
        session.close()

        return {'msg': 'el trayecto fue eliminado'}
