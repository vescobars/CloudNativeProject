""" Global Exceptions """


class UniqueConstraintViolatedException(Exception):
    """A uniqueness constraint in the database was violated"""''


class UserNotFoundException(Exception):
    """The requested user was not found"""


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class IncorrectUserPasswordException(Exception):
    """The username or password given was invalid"""


class ExpiredTokenException(Exception):
    """The token has already expired"""


class InvalidTokenException(Exception):
    """The token was not found, it might be expired or unauthentic"""
