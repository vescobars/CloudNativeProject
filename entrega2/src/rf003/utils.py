""" Utils for RF003 """
from datetime import datetime

from src.exceptions import PostIsFromSameUserException, RouteStartDateExpiredException


class RF003:

    @staticmethod
    def validate_same_user_or_dates(route, user_id):
        if datetime.utcnow() > route.plannedStartDate:
            raise RouteStartDateExpiredException()
        if datetime.utcnow() > route.plannedStartDate:
            raise RouteStartDateExpiredException()
