""" File to store global constants and simple utils """
from datetime import datetime

TOKEN_LENGTH_BYTES = 128
DEFAULT_SALT_LENGTH_BYTES = 32


def datetime_to_str(date: datetime) -> str:
    """Returns a datetime as string in the correct ISO format"""
    return date.isoformat(sep="T", timespec="seconds").split("+")[0]
