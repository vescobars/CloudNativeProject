""" Global Exceptions """


class UniqueConstraintViolatedException(Exception):
    """A uniqueness constraint in the database was violated"""''


class UtilityNotFoundException(Exception):
    """The requested utility was not found"""


class InvalidRequestException(Exception):
    """The request body was empty or otherwise invalid"""


class UnauthorizedUserException(Exception):
    """The provided credentials were valid, but were rejected due to lack of authorization or expiration"""
