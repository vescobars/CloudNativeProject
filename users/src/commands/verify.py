from .base_command import BaseCommannd
from ..models.user import User
from ..session import Session
from ..errors.errors import IncompleteParams, UserNotFoundError
from datetime import datetime, timedelta
from sqlalchemy import or_


class VerifyUser(BaseCommannd):
    def __init__(self, id):
        if self.is_uuid(id):
            self.user_id = id
        else:
            raise InvalidParams()

    def execute(self):
        session = Session()

        if not self.user_exists(session, self.user_id):
            session.close()
            raise UserNotFoundError()

        user = session.query(User).filter_by(id=self.user_id).one()

        if self.data.get('score') > 60 and self.data.get('RUV') == user.RUV:
            user.status = 'VERIFICADO'
        else:
            user.status = 'NO_VERIFICADO'

        user.last_updated = datetime.utcnow().date()

        session.commit()
        session.close()

    def user_exists(self, session, RUV):
        return len(session.query(User).filter_by(RUV=RUV).all()) > 0
