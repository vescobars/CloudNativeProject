""" Utils for credit cards """
import uuid
from datetime import datetime
from typing import List

import requests
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.constants import USERS_PATH, SECRET_TOKEN, TRUENATIVE_PATH, POLLING_PATH, SECRET_POLLING_TOKEN
from src.creditcards.schemas import CreateCCRequestSchema, TrueNativeRegisterCardResponseSchema, \
    UpdateCCStatusRequestSchema
from src.exceptions import UnauthorizedUserException, ExpiredCreditCardException, \
    UnexpectedResponseCodeException, CreditCardNotFoundException
from src.models import CreditCard
from src.schemas import StatusEnum
from src.utils import CommonUtils


class CreditCardUtils:

    @staticmethod
    def create_card(data: CreateCCRequestSchema, user_id: UUID4, session: Session) -> tuple[UUID4, datetime]:
        """
        Insert a new credit card into the CreditCard table

        Returns a tuple with the card's id and createdAt datetime
        """
        transaction_identifier = str(uuid.uuid4())

        CreditCardUtils.validate_cc_expiration_date(data.expirationDate)

        registration_response: TrueNativeRegisterCardResponseSchema = CreditCardUtils.register_card_truenative(
            data,
            transaction_identifier)
        CreditCardUtils.initiate_polling_call(registration_response.RUV, transaction_identifier)

        CommonUtils.check_card_token_exists(registration_response.token, session)
        credit_card = CommonUtils.create_card(
            registration_response.token,
            user_id,
            data.cardNumber[-4:],
            registration_response.RUV,
            registration_response.issuer,
            StatusEnum.POR_VERIFICAR,
            registration_response.createdAt,
            session
        )
        return credit_card.id, credit_card.createdAt

    @staticmethod
    def validate_cc_expiration_date(date: str):
        """Throws exception if date is already expired"""
        yy_raw, mm_raw = date.split("/")
        mm = int(mm_raw)
        yy = int(yy_raw)
        current_date = datetime.now()
        if current_date.year % 100 > yy or (
                current_date.year % 100 == yy and
                current_date.month > mm):
            raise ExpiredCreditCardException()

    @staticmethod
    def register_card_truenative(
            card: CreateCCRequestSchema,
            transaction_identifier: str) -> TrueNativeRegisterCardResponseSchema:
        """
        Registers card in the TrueNative microservice
        """

        request_body = {
            "card": card.model_dump(),
            "transactionIdentifier": transaction_identifier
        }

        headers = {"Authorization": 'Bearer ' + SECRET_TOKEN}
        url = TRUENATIVE_PATH.rstrip('/') + "/native/cards"
        response = requests.post(url, json=request_body, headers=headers)

        if response.status_code == 201:
            registration_data = response.json()
            return TrueNativeRegisterCardResponseSchema.model_validate(registration_data)
        else:
            # print(str(response.json()))
            raise UnexpectedResponseCodeException(response)

    @staticmethod
    def initiate_polling_call(
            ruv: str,
            transaction_identifier: str):
        """
        Initiates call to cloud function to begin polling
        """
        request_body = {
            "RUV": ruv,
            "transactionIdentifier": transaction_identifier,
            "SECRET_TOKEN": SECRET_TOKEN
        }
        headers = {"Authorization": 'Bearer ' + SECRET_POLLING_TOKEN}
        url = POLLING_PATH
        response = requests.post(url, json=request_body, headers=headers)
        if response.status_code == 200:
            print(f"Polling initiated for transaction {transaction_identifier}")
        else:
            raise UnexpectedResponseCodeException(response)

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

    @classmethod
    def update_status(cls, ruv: str, data: UpdateCCStatusRequestSchema, sess):
        """
        Updates the status of a credit card with the given data.
        """
        try:
            credit_card = sess.query(CreditCard).filter(CreditCard.ruv == ruv).one()
        except NoResultFound:
            raise CreditCardNotFoundException()

        credit_card.status = data.status.value
        credit_card.updateAt = datetime.now()
        sess.commit()
        return credit_card
