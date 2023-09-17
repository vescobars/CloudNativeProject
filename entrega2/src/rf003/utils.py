""" Utils for RF003 """
from datetime import datetime
from uuid import UUID
import requests

from src.constants import POSTS_PATH, ROUTES_PATH
from src.exceptions import PostIsFromSameUserException, RouteStartDateExpiredException, RouteEndDateExpiredException, \
    RouteExpireAtDateExpiredException


class RF003:
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
        if len(posts) >= 1:
            raise RouteStartDateExpiredException()

    @staticmethod
    def validate_same_user_or_dates(route, expireAt):
        if route.plannedStartDate > datetime.utcnow():
            raise RouteStartDateExpiredException()
        if datetime.utcnow() > route.plannedEndDate:
            raise RouteEndDateExpiredException()
        if datetime.utcnow() > expireAt:
            raise RouteExpireAtDateExpiredException()
        if expireAt > route.plannedStartDate:
            raise RouteExpireAtDateExpiredException()
