""" Utils for RF003 """
from datetime import datetime
from typing import List, Optional
from uuid import UUID

import requests

from src.constants import POSTS_PATH, ROUTES_PATH
from src.exceptions import RouteStartDateExpiredException, RouteEndDateExpiredException, \
    RouteExpireAtDateExpiredException, InvalidParamsException, UnauthorizedUserException, \
    InvalidCredentialsUserException, PostFoundInRouteException
from src.schemas import PostSchema


class RF003:

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

        if expire is not None:
            posts_url += f"expire={expire}&"

        if route_id is not None:
            posts_url += f"route={route_id}&"

        if owner is not None:
            posts_url += f"owner={owner}&"

        if posts_url.endswith('&'):
            posts_url = posts_url[:-1]

        response = requests.get(posts_url, headers={"Authorization": bearer_token})
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
        if len(posts) > 1:
            raise PostFoundInRouteException()

    @staticmethod
    def validate_same_user_or_dates(route, expire_at):
        if route.plannedStartDate < datetime.utcnow():
            raise RouteStartDateExpiredException()
        if datetime.utcnow() > route.plannedEndDate:
            raise RouteEndDateExpiredException()
        if datetime.utcnow() > expire_at:
            raise RouteExpireAtDateExpiredException()
        if expire_at > route.plannedStartDate:
            raise RouteExpireAtDateExpiredException()
