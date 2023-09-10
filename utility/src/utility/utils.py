""" Utils for users """
import requests
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session

from src.constants import USERS_PATH
from src.exceptions import UniqueConstraintViolatedException, UtilityNotFoundException, UnauthorizedUserException
from src.models import Utility
from src.schemas import UtilitySchema
from src.utility.schemas import CreateUtilityRequestSchema, BagSize, UpdateUtilityRequestSchema


def get_utility(offer: float, size: BagSize, bag_cost: int) -> float:
    """Calculates utility score"""
    bag_occupation = 1.0
    if size == BagSize.MEDIUM:
        bag_occupation = 0.5
    if size == BagSize.SMALL:
        bag_occupation = 0.25
    return offer - (bag_occupation * float(bag_cost))


class Utilities:

    @staticmethod
    def create_utility(data: CreateUtilityRequestSchema, session: Session) -> UtilitySchema:
        """
        Insert a new utility into the Utilities table
        """
        new_utility = None
        utility_value = get_utility(data.offer, data.size, data.bag_cost)
        with session:
            current_time = datetime.now(timezone.utc)
            try:
                new_utility = Utility(
                    offer_id=data.offer_id,
                    utility=utility_value,
                    createdAt=current_time,
                    updateAt=current_time
                )

                session.add(new_utility)
                session.commit()
            except IntegrityError as e:
                raise UniqueConstraintViolatedException(e)
        return new_utility

    @staticmethod
    def update_utility(offer_id: str, data: UpdateUtilityRequestSchema, sess: Session) -> bool:
        """Updates utility value given a certain offer_id"""
        try:
            retrieved_utility = sess.execute(
                select(Utility).where(Utility.id == offer_id)
            ).scalar_one()

            updated = False
            utility_value = get_utility(data.offer, data.size, data.bag_cost)
            if retrieved_utility.utility != utility_value:
                retrieved_utility.utility = utility_value
                updated = True

            if updated:
                retrieved_utility.updateAt = datetime.now(timezone.utc)
                sess.commit()
            return updated
        except (NoResultFound, DataError, TypeError):
            raise UtilityNotFoundException()

    @staticmethod
    def get_utility(offer_id: str, sess: Session) -> UtilitySchema:
        """
        Retrieves utility from the database
        Args:
            offer_id:
            sess:

        Returns:
            utility schema
        """
        try:
            retrieved_utility: Utility = sess.execute(
                select(Utility).where(Utility.id == offer_id)
            ).scalar_one()
        except NoResultFound:
            raise UtilityNotFoundException()

        return UtilitySchema(
            offer_id=retrieved_utility.offer_id,
            utility=retrieved_utility.utility,
            createdAt=retrieved_utility.createdAt,
            updateAt=retrieved_utility.updateAt
        )

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
