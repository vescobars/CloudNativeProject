import os

import requests

from .base_command import BaseCommannd
from ..models.user import User, UserSchema, CreatedUserJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams, UserAlreadyExists
from sqlalchemy import or_


class CreateUser(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
            posted_user = UserSchema(
                only=('username', 'email', 'phoneNumber',
                      'dni', 'fullName', 'password')
            ).load(self.data)
            user = User(**posted_user)
            session = Session()

            if self.username_exist(session, self.data['username']) or self.email_exist(session, self.data['email']):
                session.close()
                raise UserAlreadyExists()

            response = self.true_native_request(user)
            user.RUV = response.RUV

            session.add(user)
            session.commit()

            new_user = CreatedUserJsonSchema().dump(user)
            session.close()

            return new_user
        except TypeError:
            raise IncompleteParams()

    def username_exist(self, session, username):
        return len(session.query(User).filter_by(username=username).all()) > 0

    def email_exist(self, session, email):
        return len(session.query(User).filter_by(email=email).all()) > 0

    def true_native_request(self, user):
        secret_token = os.environ['SECRET_TOKEN']
        native_Path = os.environ['NATIVE_PATH']
        user_Path = os.environ['USERS_PATH']
        transaction_identifier = user.id
        user_webhook = user_Path+"/hook_users/"+user.id

        url = native_Path+"/native/verify"
        headers = {
            'Authorization': f'Bearer {secret_token}',
            'Content-Type': 'application/json',
        }
        request_body = {
            "user": {
                "email": user.email,
                "dni": user.dni,
                "fullName": user.fullName,
                "phone": user.phoneNumber
            },
            "transactionIdentifier": transaction_identifier,
            "userIdentifier": user.id,
            "userWebhook": user_webhook
        }
        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 201:
            return response.json()
        else:
            # Handle other response codes as needed
            raise Exception("Unexpected response: " + response.text)


