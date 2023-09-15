""" Utils for RF003 """
from datetime import datetime

from src.exceptions import PostIsFromSameUserException, RouteStartDateExpiredException, RouteEndDateExpiredException, \
    RouteExpireAtDateExpiredException


class RF003:

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
