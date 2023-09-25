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


class UniqueConstraintViolatedException(ResponseException):
    """A unique constraint has been violated"""
    status_code = 500
    msg = "A unique constraint has been violated"


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class InvalidParamsException(ResponseException):
    code = 400
    msg = "Invalid Parameters"


class ExpiredCreditCardException(ResponseException):
    """Credit card is already expired"""
    code = 412
    msg = "Credit card is already expired"


class InvalidCredentialsUserException(ResponseException):
    """The provided credentials were not valid or missing"""
    status_code = 403
    msg = "Credentials were not valid, or were missing"


class UnauthorizedUserException(ResponseException):
    """The provided credentials were valid, but were rejected due to lack of authorization or expiration"""
    status_code = 401
    msg = "Credentials were correctly formatted, but were rejected by the server"
