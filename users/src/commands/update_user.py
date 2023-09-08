from .base_command import BaseCommannd
from ..models.user import User
from ..session import Session
from ..errors.errors import IncompleteParams, UserNotFoundError
from sqlalchemy import or_


class UpdateUser(BaseCommannd):
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def execute(self):
        session = Session()

        if not self.user_exists(session, self.id):
            session.close()
            raise UserNotFoundError()

        if not self.update_data_valid():
            session.close()
            raise IncompleteParams()

        user = session.query(User).filter_by(id=self.id).one()
        for key, value in self.data.items():
            setattr(user, key, value)

        session.commit()
        session.close()
        return {'msg': 'el usuario ha sido actualizado'}

    def user_exists(self, session, id):
        return len(session.query(User).filter_by(id=id).all()) > 0

    def update_data_valid(self):
        return any(key in self.data for key in ['status', 'dni', 'fullName', 'phoneNumber'])
