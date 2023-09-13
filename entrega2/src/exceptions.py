""" Global Exceptions """


class ResponseException(Exception):
    """Base exception that should be used to return an error response"""
    status_code: int
    msg: str = ""


class UniqueConstraintViolatedException(Exception):
    """A uniqueness constraint in the database was violated"""''


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class PostIsFromSameUserException(ResponseException):
    """The requested post is from the same user making an offer"""
    status_code = 412
    msg = "The requested post is from the same user making an offer"


class PostExpiredException(ResponseException):
    """The requested post is already expired"""
    status_code = 412
    msg = "The requested post is already expired"


class PostNotFoundException(ResponseException):
    """The requested post was not found"""
    status_code = 404
    msg = "Credentials ere not valid, or were missing"


class InvalidCredentialsUserException(ResponseException):
    """The provided credentials were not valid or missing"""
    status_code = 403
    msg = "Credentials ere not valid, or were missing"


class UnauthorizedUserException(ResponseException):
    """The provided credentials were valid, but were rejected due to lack of authorization or expiration"""
    status_code = 401
    msg = "Credentials were correctly formatted, but were rejected by the server"
