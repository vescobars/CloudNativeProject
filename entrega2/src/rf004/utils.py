""" Utils for RF004 """
from datetime import datetime
from uuid import UUID

import requests

from src.constants import OFFERS_PATH, UTILITY_PATH
from src.exceptions import FailedCreatedUtilityException, PostIsFromSameUserException, PostExpiredException
from src.rf004.schemas import CreateUtilityRequestSchema


class RF004:

    @staticmethod
    def delete_offer(offer_id: UUID, bearer_token: str):
        """
        Asks offer endpoint to delete offer
        """
        offers_url = OFFERS_PATH.rstrip("/") + f"/offers/{str(offer_id)}"

        requests.delete(offers_url, headers={"Authorization": bearer_token})

    @staticmethod
    def create_utility(data: CreateUtilityRequestSchema, bearer_token: str):
        """
        Asks Utility endpoint to create new Utility
        """
        utility_url = UTILITY_PATH.rstrip("/") + "/utility"

        response = requests.post(utility_url, json=data.model_dump(mode='json'),
                                 headers={"Authorization": bearer_token})
        if response.status_code != 201:
            raise FailedCreatedUtilityException()

    @staticmethod
    def validate_same_user_or_expired(post, user_id):
        if str(post.userId) == user_id:
            raise PostIsFromSameUserException()
        if datetime.utcnow() > post.expireAt:
            raise PostExpiredException()
