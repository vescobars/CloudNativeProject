""" Utils for RF005 """
from typing import List
from uuid import UUID

import requests

from src.constants import OFFERS_PATH, UTILITY_PATH
from src.exceptions import UnauthorizedUserException, InvalidCredentialsUserException, PostUserOwnerMismatchException
from src.rf005.schemas import ImprovedRouteSchema, Location, ScoredOfferSchema
from src.schemas import RouteSchema, PostSchema


class RF005:

    @staticmethod
    def get_filtered_offers(post_id: UUID, bearer_token: str) -> List[ScoredOfferSchema]:
        offers_url = OFFERS_PATH.rstrip("/") + "/offers"
        response_filtered = requests.get(
            offers_url, headers={"Authorization": bearer_token},
            params={
                "post": str(post_id)
            }
        )
        if response_filtered.status_code == 401:
            raise UnauthorizedUserException()
        elif response_filtered.status_code == 403:
            raise InvalidCredentialsUserException()

        response_body = response_filtered.json()
        response_set = {res['id']: res for res in response_body}

        utilities_url = UTILITY_PATH.rstrip("/") + "/utility/list"
        response_sorted = requests.post(
            utilities_url, headers={"Authorization": bearer_token},
            json=list(response_set.keys())
        )

        filtered_sorted_offers = []
        for offer in response_sorted.json():
            scored_offer = response_set[offer["offer_id"]]
            scored_offer["score"] = offer["utility"]
            filtered_sorted_offers.append(ScoredOfferSchema.model_validate(scored_offer))

        return filtered_sorted_offers

    @staticmethod
    def get_detailed_route(route: RouteSchema):
        """
        Converts a simple route to the improved schema desired by RF005
        """

        return ImprovedRouteSchema(
            id=route.id,
            flightId=route.flightId,
            origin=Location(
                airportCode=route.sourceAirportCode,
                country=route.sourceCountry
            ),
            destiny=Location(
                airportCode=route.destinyAirportCode,
                country=route.destinyCountry
            ),
            bagCost=route.bagCost
        )

    @staticmethod
    def validate_post(post: PostSchema, user_id: str):
        """Makes sure user is authorized to see this post"""
        if user_id != str(post.userId):
            raise PostUserOwnerMismatchException()
