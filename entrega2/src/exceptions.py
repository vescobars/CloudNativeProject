""" Global Exceptions """
from typing import Optional


class ResponseException(Exception):
    """Base exception that should be used to return an error response"""
    status_code: int
    msg: str = ""
    detail: Optional[dict] = None


class UnexpectedResponseCodeException(ResponseException):
    """The expected response status_code was not received."""

    def __init__(self, original_response):
        self.detail = {"received_status_code": original_response.status_code}

    status_code = 500
    msg = "The expected response status_code was not received."


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class OfferInvalidValuesException(ResponseException):

    def __init__(self, original_response):
        self.detail = original_response

    """The offer has received invalid values"""
    status_code = 412
    msg = "The offer has received invalid values"


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
