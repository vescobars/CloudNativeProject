""" Global Exceptions """


class ResponseException(Exception):
    """Base exception that should be used to return an error response"""
    status_code: int
    msg: str = ""


class UniqueConstraintViolatedException(Exception):
    """A uniqueness constraint in the database was violated"""''


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class InvalidCredentialsUserException(ResponseException):
    """The provided credentials were not valid or missing"""
    status_code = 403


class UnauthorizedUserException(ResponseException):
    """The provided credentials were valid, but were rejected due to lack of authorization or expiration"""
    status_code = 401
