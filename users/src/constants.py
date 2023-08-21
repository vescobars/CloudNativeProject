""" File to store global constants and simple utils """
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

TOKEN_LENGTH_BYTES = 128
DEFAULT_SALT_LENGTH_BYTES = 32

DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_HOST = os.environ.get("DB_HOST", "0.0.0.0")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "db")


def datetime_to_str(date: datetime) -> str:
    """Returns a datetime as string in the correct ISO format"""
    return date.isoformat(sep="T", timespec="seconds").split("+")[0]
