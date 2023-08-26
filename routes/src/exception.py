""" Custom-made Global Exceptions """

class UniqueConstraintViolatedException(Exception):
    """A uniqueness constraint in the database was violated"""''


class RouteNotFoundException(Exception):
    """The requested user was not found"""


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""