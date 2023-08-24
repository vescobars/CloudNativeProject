""" Utils for routes"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session

from src.models import Route
from src.schemas import RouteSchema


class Routes:
    pass
