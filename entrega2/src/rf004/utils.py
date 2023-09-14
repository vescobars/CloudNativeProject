""" Utils for RF004 """
from datetime import datetime
from uuid import UUID

import requests

from src.constants import USERS_PATH, POSTS_PATH, ROUTES_PATH, OFFERS_PATH, UTILITY_PATH
from src.exceptions import UnauthorizedUserException, \
    PostNotFoundException, InvalidCredentialsUserException, PostExpiredException, PostIsFromSameUserException, \
    OfferInvalidValuesException, UnexpectedResponseCodeException, FailedCreatedUtilityException, \
    FailedDeletingOfferException
from src.rf004.schemas import CreateUtilityRequestSchema, BagSize, PostOfferResponseSchema
from src.schemas import PostSchema, RouteSchema


class RF004:

    def __init__(self, client):
        self.client = client

    def get_post(self, post_id: str, user_id: str, bearer_token: str) -> PostSchema:
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

        if str(post.userId) == user_id:
            raise PostIsFromSameUserException()
        if datetime.utcnow() > post.expireAt:
            raise PostExpiredException()

        return post

    def get_route(self, route_id: UUID, bearer_token: str) -> RouteSchema:
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

        route = RouteSchema.model_validate(response.json())

        return route

    def create_offer(self, post_id: UUID, description: str, size: BagSize, fragile: bool, offer: float,
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

    def delete_offer(self, offer_id: UUID, bearer_token: str):
        """
        Asks offer endpoint to delete offer
        """
        offers_url = OFFERS_PATH.rstrip("/") + f"/offers/{str(offer_id)}"

        response = requests.delete(offers_url, headers={"Authorization": bearer_token})

        if response.status_code != 200:
            raise FailedDeletingOfferException()

    def create_utility(self, data: CreateUtilityRequestSchema, bearer_token: str):
        """
        Asks Utility endpoint to create new Utility
        """
        utility_url = UTILITY_PATH.rstrip("/") + "/utility"

        response = requests.post(utility_url, json=data.model_dump(mode='json'),
                                         headers={"Authorization": bearer_token})
        if response.status_code != 201:
            raise FailedCreatedUtilityException()

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
