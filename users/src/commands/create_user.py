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

    def true_native_request(self, user, newUser):
        secret_token = os.environ['SECRET_TOKEN']
        native_Path = os.environ['NATIVE_PATH']
        user_Path = os.environ['USERS_PATH']
        transaction_identifier = generate_transaction_identifier()
        user_webhook = user_Path+"/hook_users/"+newUser.id

        url = native_Path+"/native/verify"
        headers = {
            'Authorization': f'Bearer {secret_token}',
            'Content-Type': 'application/json',
        }
        request_body = {
            "user": {
                "email": user.email,
                "dni": user.dni,
                "fullName": user.full_name,
                "phone": user.phone
            },
            "transactionIdentifier": transaction_identifier,
            "userIdentifier": newUser.id,
            "userWebhook": user_webhook
        }
        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 201:
            return response.json()
        elif response.status_code == 400:
            raise UserAlreadyExists()
        elif response.status_code == 401:
            raise UserAlreadyExists()
        elif response.status_code == 403:
            raise UserAlreadyExists()
        elif response.status_code == 409:
            raise UserAlreadyExists()
        else:
            # Handle other response codes as needed
            raise Exception("Unexpected response: " + response.text)

    def generate_transaction_identifier(self):
        timestamp = int(time.time() * 1000)
        unique_id = str(uuid.uuid4().hex)
        return f"{timestamp}-{unique_id}"


