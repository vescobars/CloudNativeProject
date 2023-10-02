from .base_command import BaseCommannd
from ..models.user import User
from ..session import Session
from ..errors.errors import IncompleteParams, UserNotFoundError, EmailSendError
from datetime import datetime, timedelta
from sqlalchemy import or_
import requests


class VerifyUser(BaseCommannd):
    def __init__(self, id):
        if self.is_uuid(id):
            self.user_id = id
        else:
            raise IncompleteParams()

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

        response_mail = self.send_Email(user)

        if response_mail.status_code != 200:
            raise EmailSendError()

        session.commit()
        session.close()

    def user_exists(self, session, RUV):
        return len(session.query(User).filter_by(RUV=RUV).all()) > 0

    def send_Email(self, user):
        url = "https://us-central1-miso-grupo-17.cloudfunctions.net/send_email_notification"
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "subject": "Verification Process",
            "content": f"Your verification process ended with {user.status} status",
            "recipient": "vescobars2001@gmail.com"
        }

        response = requests.post(url, headers=headers, json=data)

        return response
