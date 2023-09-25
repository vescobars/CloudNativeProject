""" Utils for credit cards """
from datetime import datetime, timezone
from typing import List

import requests
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from src.constants import USERS_PATH
from src.creditcards.schemas import CreateCCRequestSchema
from src.exceptions import UniqueConstraintViolatedException, UnauthorizedUserException, ExpiredCreditCardException
from src.schemas import StatusEnum
from src.utils import CommonUtils


class CreditCardUtils:

    @staticmethod
    def create_card(data: CreateCCRequestSchema, user_id: UUID4, session: Session) -> tuple[UUID4, datetime]:
        """
        Insert a new credit card into the CreditCard table
        """
        CreditCardUtils.validate_cc_expiration_date(data.expirationDate)
        token = "TO BE DELIVERED BY TRUENATIVE"
        ruv = "TO BE DELIVERED BY TRUENATIVE"
        issuer = "TO BE DELIVERED BY TRUENATIVE"
        created_at = "TO BE DELIVERED BY TRUENATIVE"
        CommonUtils.check_card_token_exists(token, session)
        credit_card = CommonUtils.create_card(
            token,
            user_id,
            data.cardNumber[-4:],
            ruv,
            issuer,
            StatusEnum.POR_VERIFICAR,
            created_at,
            session
        )

    @staticmethod
    def validate_cc_expiration_date(date: str):
        """Throws exception if date is already expired"""
        yy_raw, mm_raw = date.split("/")
        mm = int(mm_raw)
        yy = int(yy_raw)
        current_date = datetime.now()
        if current_date.year % 100 > yy:
            raise ExpiredCreditCardException()
        elif (current_date.year % 100 == yy and
              current_date.month > mm):
            raise ExpiredCreditCardException()

    @staticmethod
    def get_utilities(offer_ids: List[UUID4], sess: Session) -> list[UtilitySchema]:
        """
        Retrieves utilities from the database with the given offer ids.

        """
        try:
            retrieved_utilities_raw = list(sess.execute(
                select(Utility)
                .where(Utility.offer_id.in_(offer_ids))
                .order_by(Utility.utility.desc())
            ).scalars().all())

            retrieved_utilities = [
                UtilitySchema(
                    offer_id=util.offer_id,
                    utility=util.utility,
                    createdAt=util.createdAt,
                    updateAt=util.updateAt)
                for util in retrieved_utilities_raw
            ]
        except NoResultFound:
            return []

        return retrieved_utilities if retrieved_utilities else []

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
