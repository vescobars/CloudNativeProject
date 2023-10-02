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
        self.detail = {
            "received_status_code": original_response.status_code,
            "original_response": original_response.json(),
        }

    status_code = 500
    msg = "The expected response status_code was not received."


class UniqueConstraintViolatedException(ResponseException):
    """A unique constraint has been violated"""
    status_code = 500
    msg = "A unique constraint has been violated"


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class InvalidParamsException(ResponseException):
    status_code = 400
    msg = "Invalid Parameters"


class ExpiredCreditCardException(ResponseException):
    """Credit card is already expired"""
    status_code = 412
    msg = "Credit card is already expired"


class CreditCardNotFoundException(ResponseException):
    """Credit card ruv was not found"""
    status_code = 404
    msg = "Credit card ruv was not found"


class CreditCardTokenExistsException(ResponseException):
    """Credit card token matches one already in the database"""
    status_code = 409
    msg = "Credit card token matches one already in the database"


class InvalidCredentialsUserException(ResponseException):
    """The provided credentials were not valid or missing"""
    status_code = 403
    msg = "Credentials were not valid, or were missing"


class UnauthorizedUserException(ResponseException):
    """The provided credentials were valid, but were rejected due to lack of authorization or expiration"""
    status_code = 401
    msg = "Credentials were correctly formatted, but were rejected by the server"
