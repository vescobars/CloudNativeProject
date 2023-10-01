from .base_command import BaseCommannd
from ..models.user import User
from ..session import Session
from ..errors.errors import IncompleteParams, UserNotFoundError
from sqlalchemy import or_


class VerifyUser(BaseCommannd):
    def __init__(self, user_id):
        if self.is_uuid(user_id):
            self.route_id = user_id
        else:
            raise InvalidParams()

    def execute(self):
        session = Session()

        if not self.user_exists(session, self.route_id):
            session.close()
            raise UserNotFoundError()

        user = session.query(User).filter_by(id=self.route_id).one()

        if self.data.get('task_status') == 'ACCEPTED':
            user.status = 'VERIFICADO'
        else:
            user.status = 'NO_VERIFICADO'

        session.commit()
        session.close()

    def user_exists(self, session, id):
        return len(session.query(User).filter_by(id=id).all()) > 0
