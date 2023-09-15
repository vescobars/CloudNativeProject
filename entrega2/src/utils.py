""" Utils for RF004 """
from uuid import UUID
from datetime import datetime

import requests

from src.constants import USERS_PATH, POSTS_PATH, ROUTES_PATH, OFFERS_PATH
from src.exceptions import UnauthorizedUserException, \
    PostNotFoundException, InvalidCredentialsUserException, OfferInvalidValuesException, \
    UnexpectedResponseCodeException, RouteNotFoundException
from src.rf003.schemas import CreatedRouteSchema
from src.rf004.schemas import PostOfferResponseSchema
from src.schemas import PostSchema, RouteSchema, BagSize


class CommonUtils:

    @staticmethod
    def get_post(post_id: str, user_id: str, bearer_token: str) -> PostSchema:
        """
        Retrieves a post from the Posts endpoint
        :param post_id: the post's UUID
        :param user_id: the uuid of the user
        :param bearer_token: the bearer token with which the request is authenticated
        :return: a post object
        """
        posts_url = POSTS_PATH.rstrip("/") + f"/posts/{post_id}"
        response = requests.get(posts_url, headers={"Authorization": bearer_token})
        if response.status_code == 404:
            raise PostNotFoundException()
        elif response.status_code == 401:
            raise UnauthorizedUserException()
        elif response.status_code == 403:
            raise InvalidCredentialsUserException()
        post = PostSchema.model_validate(response.json())

        return post

    @staticmethod
    def get_route(route_id: UUID, bearer_token: str) -> RouteSchema:
        """
        Retrieves a route from the Routes endpoint
        :param route_id: the route's UUID
        :param bearer_token: the bearer token with which the request is authenticated
        :return: a route object
        """
        routes_url = ROUTES_PATH.rstrip("/") + f"/routes/{str(route_id)}"
        response = requests.get(routes_url, headers={"Authorization": bearer_token})
        if response.status_code == 401:
            raise UnauthorizedUserException()
        elif response.status_code == 403:
            raise InvalidCredentialsUserException()
        elif response.status_code == 404:
            raise RouteNotFoundException();

        route = RouteSchema.model_validate(response.json())

        return route

    @staticmethod
    def create_offer(post_id: UUID, description: str, size: BagSize, fragile: bool, offer: float,
                     bearer_token: str) -> PostOfferResponseSchema:
        """
        Asks offer endpoint to create new offer
        """
        offers_url = OFFERS_PATH.rstrip("/") + "/offers"

        payload = {
            "postId": str(post_id),
            "description": description,
            "size": size.value,
            "fragile": fragile,
            "offer": offer
        }

        response = requests.post(offers_url, json=payload, headers={"Authorization": bearer_token})
        if response.status_code == 401:
            raise UnauthorizedUserException()
        elif response.status_code == 403:
            raise InvalidCredentialsUserException()
        elif response.status_code == 412:
            raise OfferInvalidValuesException(response.json())
        elif response.status_code != 201:
            raise UnexpectedResponseCodeException(response)

        offer: PostOfferResponseSchema = PostOfferResponseSchema.model_validate(response.json())

        return offer

    @staticmethod
    def create_route(flightId: str, sourceAirportCode: str, sourceCountry: str,
                     destinyAirportCode: str, destinyCountry: str, bagCost: int,
                     plannedStartDate: datetime, plannedEndDate: datetime, bearer_token: str) -> CreatedRouteSchema:
        """
        Asks offer endpoint to create new offer
        """
        routes_url = ROUTES_PATH.rstrip("/") + "/routes"

        payload = {
            "flightId": flightId,
            "sourceAirportCode": sourceAirportCode,
            "sourceCountry": sourceCountry,
            "destinyAirportCode": destinyAirportCode,
            "destinyCountry": destinyCountry,
            "bagCost": bagCost,
            "plannedStartDate": plannedStartDate,
            "plannedEndDate": plannedEndDate
        }

        response = requests.post(routes_url, json=payload, headers={"Authorization": bearer_token})
        if response.status_code == 401:
            raise UnauthorizedUserException()
        elif response.status_code == 403:
            raise InvalidCredentialsUserException()
        elif response.status_code == 412:
            raise OfferInvalidValuesException(response.json())
        elif response.status_code == 412:
            response_json = response.json()
            error_description = response_json.get("description")
            if error_description == "Las fechas del trayecto no son válidas":
                raise OfferInvalidValuesException(response_json)
            elif error_description == "Flight ID already exists":
                raise OfferInvalidValuesException(response_json)
        elif response.status_code != 201:
            raise UnexpectedResponseCodeException(response)

        route: CreatedRouteSchema = CreatedRouteSchema.model_validate(response.json())

        return route

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
