""" Custom-made Global Exceptions """


class UniqueConstraintViolatedException(Exception):
    """A uniqueness constraint in the database was violated"""''


class RouteNotFoundException(Exception):
    """The requested user was not found"""


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class ExpiredTokenException(Exception):
    """The token has already expired"""


class InvalidTokenException(Exception):
    """The token was not found, it might be expired or unauthentic"""


class ErrorResponseException(Exception):
    def __init__(self, status_code: int = 400, detail: dict = None):
        if detail is None:
            detail = {}
        self.status_code = status_code
        self.detail = detail
