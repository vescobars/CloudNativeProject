""" Utils"""
from datetime import datetime, timezone

import requests
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.constants import USERS_PATH
from src.exceptions import UnauthorizedUserException, UniqueConstraintViolatedException
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
            session: Session
    ) -> CreditCard:
        """Insert new credit card into the table"""
        new_cc = None
        current_time = datetime.now(timezone.utc)
        try:
            new_cc = CreditCard(
                token=token,
                userId=user_id,
                lastFourDigits=last_four_digits,
                ruv=ruv,
                issuer=issuer.value,
                status=status.value,
                createdAt=current_time,
                updateAt=current_time,
            )

            session.add(new_cc)
            session.commit()
        except IntegrityError as e:
            raise UniqueConstraintViolatedException(e)
        return new_cc

    @staticmethod
    def authenticate_user(bearer_token: str) -> str:
        headers = {"Authorization": 'Bearer ' + bearer_token}
        url = USERS_PATH.rstrip('/') + "/users/me"
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data["id"]
            return user_id
        else:
            raise UnauthorizedUserException()
