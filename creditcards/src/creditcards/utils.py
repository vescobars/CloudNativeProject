""" Utils for RF003 """
from datetime import datetime
from typing import List, Optional
from uuid import UUID

import requests

from src.constants import POSTS_PATH, ROUTES_PATH
from src.exceptions import RouteStartDateExpiredException, RouteEndDateExpiredException, \
    RouteExpireAtDateExpiredException, InvalidParamsException, UnauthorizedUserException, \
    InvalidCredentialsUserException, PostFoundInRouteException


class CreditCardUtils:

    @staticmethod
    def get_post_filtered(expire: Optional[str], route_id: str, owner: str, bearer_token: str) -> List[PostSchema]:
        """
        Retrieves a post from the Posts endpoint
        :param expire: if the post expires
        :param route_id: the route's UUID associated with the post
        :param owner: the post's owner UUID
        :param bearer_token: the bearer token with which the request is authenticated
        :return: a post object
        """

        posts_url = POSTS_PATH.rstrip("/") + "/posts?"

        params = {
            "expire": expire,
            "route": route_id,
            "owner": owner,
        }

        response = requests.get(posts_url, headers={"Authorization": bearer_token}, params=params)
        if response.status_code == 404:
            raise InvalidParamsException()
        elif response.status_code == 401:
            raise UnauthorizedUserException()
        elif response.status_code == 403:
            raise InvalidCredentialsUserException()

        posts = []
        for post in response.json():
            posts.append(PostSchema.model_validate(post))

        return posts

    @staticmethod
    def delete_route(route_id: UUID, bearer_token: str):
        """
        Asks post endpoint to delete post
        """
        route_url = ROUTES_PATH.rstrip("/") + f"/routes/{str(route_id)}"
        requests.delete(route_url, headers={"Authorization": bearer_token})

    @staticmethod
    def delete_post(post_id: UUID, bearer_token: str):
        """
        Asks post endpoint to delete post
        """
        posts_url = POSTS_PATH.rstrip("/") + f"/posts/{str(post_id)}"
        requests.delete(posts_url, headers={"Authorization": bearer_token})

    @staticmethod
    def validate_post(posts):
        if len(posts) > 0:
            raise PostFoundInRouteException()

    @staticmethod
    def validate_same_user_or_dates(
            planned_start_date_raw: datetime,
            planned_end_date_raw: datetime,
            expire_at_raw: datetime):

        planned_start_date_naive = planned_start_date_raw.replace(tzinfo=None)
        planned_end_date_naive = planned_end_date_raw.replace(tzinfo=None)
        expire_at_naive = expire_at_raw.replace(tzinfo=None)
        dt_now_naive = datetime.utcnow()

        if planned_start_date_naive < dt_now_naive:
            raise RouteStartDateExpiredException()
        if planned_end_date_naive < dt_now_naive:
            raise RouteEndDateExpiredException()
        if dt_now_naive > expire_at_naive:
            raise RouteExpireAtDateExpiredException()
        if expire_at_naive > planned_start_date_naive:
            raise RouteExpireAtDateExpiredException()
