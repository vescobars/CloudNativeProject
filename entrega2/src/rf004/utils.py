""" Utils for RF004 """
from datetime import datetime, timezone

import requests
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session

from src.constants import USERS_PATH, POSTS_PATH, ROUTES_PATH
from src.exceptions import UniqueConstraintViolatedException, UtilityNotFoundException, UnauthorizedUserException, \
    PostNotFoundException, InvalidCredentialsUserException, PostExpiredException, PostIsFromSameUserException
from src.models import Utility
from src.rf004.schemas import check_uuid4
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
    async def get_route(cls, route_id: str, bearer_token: str) -> RouteSchema:
        """
        Retrieves a route from the Routes endpoint
        :param route_id: the route's UUID
        :param bearer_token: the bearer token with which the request is authenticated
        :return: a route object
        """
        routes_url = ROUTES_PATH.rstrip("/") + f"/routes/{route_id}"
        response = await cls.client.get(routes_url, headers={"Authorization": bearer_token})
        if response.status_code == 401:
            raise UnauthorizedUserException()
        elif response.status_code == 403:
            raise InvalidCredentialsUserException()

        route = RouteSchema.model_validate(response.json())

        return route

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
            raise UniqueConstraintViolatedException(e)
        return new_utility

    @staticmethod
    def update_utility(offer_id: str, data: UpdateUtilityRequestSchema, sess: Session) -> bool:
        """Updates utility value given a certain offer_id"""
        try:
            retrieved_utility = sess.execute(
                select(Utility).where(Utility.offer_id == offer_id)
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
                select(Utility).where(Utility.offer_id == offer_id)
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
