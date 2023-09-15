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


class FailedCreatedUtilityException(Exception):
    """Creating utility did not succeed"""


class SuccessfullyDeletedOfferException(ResponseException):
    """Fired after a utility failed to be created, so a corrective offer deletion is successfully issued"""
    status_code = 500
    detail = "Utility failed to be stored, offer deleted"


class FailedDeletingOfferException(ResponseException):
    """Deleting an offer did not succeed"""
    status_code = 500
    msg = "Deleting an offer did not succeed"


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class OfferInvalidValuesException(ResponseException):

    def __init__(self, original_response):
        self.detail = original_response

    """The offer has received invalid values"""
    status_code = 412
    msg = "The offer has received invalid values"


class PostUserOwnerMismatchException(ResponseException):
    """The user is not the owner of the requested post"""
    status_code = 403
    msg = "The user is not the owner of the requested post"


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
    msg = "The requested post doesnt exist"


class PostNotFoundException(ResponseException):
    """The requested post was not found"""
    status_code = 404
    msg = "The requested post doesnt exist"


class PostUniqueException(ResponseException):
    """There is one or more posts that assigned to your route"""
    status_code = 409
    msg = "There is one or more posts that assigned to your route"


class InvalidParamsException(ResponseException):
    code = 400
    msg = "Invalid Parameters"


class InvalidCredentialsUserException(ResponseException):
    """The provided credentials were not valid or missing"""
    status_code = 403
    msg = "Credentials were not valid, or were missing"


class UnauthorizedUserException(ResponseException):
    """The provided credentials were valid, but were rejected due to lack of authorization or expiration"""
    status_code = 401
    msg = "Credentials were correctly formatted, but were rejected by the server"


class RouteStartDateExpiredException(ResponseException):
    """The route's start date is invalid"""
    status_code = 412
    msg = "The route's start date is invalid"


class RouteEndDateExpiredException(ResponseException):
    """The route's end date is invalid"""
    status_code = 412
    msg = "The route's end date is invalid"


class RouteExpireAtDateExpiredException(ResponseException):
    """The post's expire at date is invalid"""
    status_code = 412
    msg = "The post's expire at date is invalid"


class RouteNotFoundException(ResponseException):
    """The requested route was not found"""
    status_code = 404
    msg = "The requested route was not found"
