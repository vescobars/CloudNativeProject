""" Utils for RF004 """
from datetime import datetime, timezone
from uuid import UUID

import requests
from httpx import AsyncClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.constants import USERS_PATH, POSTS_PATH, ROUTES_PATH, OFFERS_PATH
from src.exceptions import UniqueConstraintViolatedException, UnauthorizedUserException, \
    PostNotFoundException, InvalidCredentialsUserException, PostExpiredException, PostIsFromSameUserException, \
    OfferInvalidValuesException, UnexpectedResponseCodeException
from src.models import Utility
from src.rf004.schemas import CreateUtilityRequestSchema, BagSize, PostOfferResponseSchema
from src.schemas import UtilitySchema, PostSchema, RouteSchema


class RF004:
    client: AsyncClient

    def __init__(self, client):
        self.client = client

    @classmethod
    async def get_post(cls, post_id: str, user_id: str, bearer_token: str) -> PostSchema:
        """
        Retrieves a post from the Posts endpoint
        :param post_id: the post's UUID
        :param user_id: the uuid of the user
        :param bearer_token: the bearer token with which the request is authenticated
        :return: a post object
        """
        posts_url = POSTS_PATH.rstrip("/") + f"/posts/{post_id}"
        response = await cls.client.get(posts_url, headers={"Authorization": bearer_token})
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

    @classmethod
    async def get_route(cls, route_id: UUID, bearer_token: str) -> RouteSchema:
        """
        Retrieves a route from the Routes endpoint
        :param route_id: the route's UUID
        :param bearer_token: the bearer token with which the request is authenticated
        :return: a route object
        """
        routes_url = ROUTES_PATH.rstrip("/") + f"/routes/{str(route_id)}"
        response = await cls.client.get(routes_url, headers={"Authorization": bearer_token})
        if response.status_code == 401:
            raise UnauthorizedUserException()
        elif response.status_code == 403:
            raise InvalidCredentialsUserException()

        route = RouteSchema.model_validate(response.json())

        return route

    @classmethod
    async def create_offer(cls, post_id: UUID, description: str, size: BagSize, fragile: bool, offer: float,
                           bearer_token: str, session: Session) -> PostOfferResponseSchema:
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

        response = await cls.client.post(offers_url, json=payload, headers={"Authorization": bearer_token})
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

    @classmethod
    def create_utility(cls, data: CreateUtilityRequestSchema, session: Session) -> UtilitySchema:
        """
        Insert a new utility into the Utilities table
        """
        new_utility = None
        utility_value = get_utility(data.offer, data.size, data.bag_cost)
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
            raise (e)
        return new_utility

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
