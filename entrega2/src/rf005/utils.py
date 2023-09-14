""" Utils for RF005 """
from typing import List
from uuid import UUID

import requests

from src.constants import OFFERS_PATH
from src.exceptions import UnauthorizedUserException, InvalidCredentialsUserException
from src.schemas import OfferSchema


class RF005:

    @staticmethod
    def get_filtered_offers(post_id: UUID, bearer_token: str) -> List[OfferSchema]:
        routes_url = OFFERS_PATH.rstrip("/") + "/offers"
        response = requests.get(
            routes_url, headers={"Authorization": bearer_token},
            params={
                "post": str(post_id),
                "owner": "me"
            }
        )
        if response.status_code == 401:
            raise UnauthorizedUserException()
        elif response.status_code == 403:
            raise InvalidCredentialsUserException()
