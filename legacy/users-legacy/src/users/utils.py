""" Utils for users """
import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from secrets import token_urlsafe
from typing import Tuple

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session

from src.constants import TOKEN_LENGTH_BYTES, DEFAULT_SALT_LENGTH_BYTES
from src.exceptions import UniqueConstraintViolatedException, UserNotFoundException, IncorrectUserPasswordException, \
    ExpiredTokenException, InvalidTokenException
from src.models import User
from src.schemas import UserSchema, UserStatusEnum
from src.users.schemas import CreateUserRequestSchema, UpdateUserRequestSchema, GenerateTokenRequestSchema, \
    GenerateTokenResponseSchema, GetUserResponseSchema


class Users:

    @staticmethod
    def create_user(data: CreateUserRequestSchema, session: Session) -> UserSchema:
        """
        Insert a new user into the Users table
        """
        new_user = None
        with session:
            current_time = datetime.now(timezone.utc)
            password_hash, salt = create_salted_hash(data.password)
            try:
                new_user = User(
                    id=uuid.uuid4(),
                    username=data.username,
                    email=data.email,
                    phoneNumber=data.phoneNumber,
                    dni=data.dni,
                    fullName=data.fullName,
                    status=UserStatusEnum.NO_VERIFICADO,

                    passwordHash=password_hash,
                    salt=salt,
                    token=Users.generate_token(TOKEN_LENGTH_BYTES),

                    expireAt=current_time,
                    createdAt=current_time,
                    updateAt=current_time
                )

                session.add(new_user)
                session.commit()
            except IntegrityError as e:
                raise UniqueConstraintViolatedException(e)
        return new_user

    @staticmethod
    def update_user(user_id: str, user_data: UpdateUserRequestSchema, sess: Session) -> bool:
        try:
            retrieved_user = sess.execute(
                select(User).where(User.id == user_id)
            ).scalar_one()

            updated = False
            for field in ['status', 'dni', 'fullName', 'phoneNumber']:
                if getattr(user_data, field):
                    setattr(retrieved_user, field, getattr(user_data, field))
                    updated = True

            if updated:
                retrieved_user.updateAt = datetime.now(timezone.utc)
                sess.commit()
            return updated
        except (NoResultFound, DataError, TypeError):
            raise UserNotFoundException()

    @staticmethod
    def generate_new_token(req_data: GenerateTokenRequestSchema,
                           sess: Session) -> GenerateTokenResponseSchema:
        """
        Checks if the given password is correct, and if so generates a new token and returns it
        Args:
            req_data:
            sess:

        Returns:
            the user id, the token and the time it will expire at
        """
        try:
            retrieved_user: User = sess.execute(
                select(User).where(User.username == req_data.username)
            ).scalar_one()

            pass_attempt_hash, _ = create_salted_hash(req_data.password, salt=retrieved_user.salt)
            if retrieved_user.passwordHash != pass_attempt_hash:
                raise IncorrectUserPasswordException()

            retrieved_user.salt = Users.generate_token(TOKEN_LENGTH_BYTES)
            retrieved_user.expireAt = datetime.now(timezone.utc) + timedelta(
                days=3
            )
            #
            retrieved_user.updateAt = datetime.now(timezone.utc)

            sess.commit()
            return GenerateTokenResponseSchema(
                id=retrieved_user.id,
                token=retrieved_user.token,
                expireAt=retrieved_user.expireAt
            )

        except (NoResultFound, DataError, TypeError):
            raise UserNotFoundException()

    @staticmethod
    def generate_token(byte_length=DEFAULT_SALT_LENGTH_BYTES) -> str:
        """
        Generates X random bytes and encodes it as a url-safe Base64 string
        Returns:
            str: cryptographically-safe random string
        """
        return token_urlsafe(byte_length)

    @staticmethod
    def get_user(user_id: str, sess: Session) -> GetUserResponseSchema:
        """
        Retrieves user from the database
        Args:
            user_id:
            sess:

        Returns:

        """
        retrieved_user: User = sess.execute(
            select(User).where(User.id == user_id)
        ).scalar_one()

        return GetUserResponseSchema(
            id=retrieved_user.id,
            username=retrieved_user.username,
            email=retrieved_user.email,
            fullName=retrieved_user.fullName,
            dni=retrieved_user.dni,
            phoneNumber=retrieved_user.phoneNumber,
            status=retrieved_user.status,
        )

    @staticmethod
    def authenticate(token: str, sess: Session) -> str:
        """
        Return user id if token is valid, return exception otherwise
        Args:
            token:
            sess:

        Returns:

        """
        try:
            retrieved_user: User = sess.execute(
                select(User).where(User.token == token)
            ).scalar_one()

            if retrieved_user.expireAt <= datetime.utcnow():
                raise ExpiredTokenException()

            return retrieved_user.id
        except NoResultFound:
            raise InvalidTokenException()


def create_salted_hash(data, salt=Users.generate_token()) -> Tuple[str, str]:
    """
    Generates a salted hash of 'data' and returns both the hash and salt.
    Salt is automatically generated if it is not provided
    Args:
        data: The text for which a salted hash will be created
        salt: The salt used for the hash. Auto-generated by default

    Returns:
        str: the hash
        str: the salt used for the hashing
    """

    concatenation = data + salt
    data_hash = hashlib.sha256(concatenation.encode(), usedforsecurity=True)
    return data_hash.hexdigest(), salt
