""" Utils"""
import uuid
from datetime import datetime

import requests
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from src.constants import USERS_PATH
from src.exceptions import UnauthorizedUserException, UniqueConstraintViolatedException, CreditCardTokenExistsException
from src.models import CreditCard
from src.schemas import IssuerEnum, StatusEnum


class CommonUtils:

    @staticmethod
    def create_card(
            token: str,
            user_id: UUID4,
            last_four_digits: str,
            ruv: str,
            issuer: IssuerEnum,
            status: StatusEnum,
            created_at: datetime,
            session: Session
    ) -> CreditCard:
        """Insert new credit card into the table"""
        new_cc = None
        try:
            new_cc = CreditCard(
                id=uuid.uuid4(),
                token=token,
                userId=user_id,
                lastFourDigits=last_four_digits,
                ruv=ruv,
                issuer=issuer.value,
                status=status.value,
                createdAt=created_at,
                updatedAt=created_at,
            )

            session.add(new_cc)
            session.commit()
        except IntegrityError as e:
            raise UniqueConstraintViolatedException(e)
        return new_cc

    @staticmethod
    def check_card_token_exists(
            token: str,
            session: Session
    ):
        """Raises exception if token already exists"""

        try:
            retrieved_cc = session.execute(
                select(CreditCard).where(CreditCard.token == token)
            ).scalar_one()
            raise CreditCardTokenExistsException()
        except NoResultFound:
            return

    @staticmethod
    def authenticate_user(bearer_token: str) -> tuple[str, str]:
        headers = {"Authorization": 'Bearer ' + bearer_token}
        url = USERS_PATH.rstrip('/') + "/users/me"
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data["id"]
            user_email = user_data["email"]
            return user_id, user_email
        else:
            raise UnauthorizedUserException()

