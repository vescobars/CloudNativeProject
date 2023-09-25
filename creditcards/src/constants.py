""" File to store global constants and simple utils """
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

TOKEN_LENGTH_BYTES = 128
DEFAULT_SALT_LENGTH_BYTES = 32

USERS_PATH = os.environ.get("USERS_PATH", "http://localhost:3000")
ROUTES_PATH = os.environ.get("ROUTES_PATH", "http://localhost:3001")
POSTS_PATH = os.environ.get("POSTS_PATH", "http://localhost:3002")
OFFERS_PATH = os.environ.get("OFFERS_PATH", "http://localhost:3003")
UTILITY_PATH = os.environ.get("UTILITY_PATH", "http://localhost:3004")

print("Connection environment variables")
print({
    "USERS_PATH": USERS_PATH,
    "ROUTES_PATH": ROUTES_PATH,
    "POSTS_PATH": POSTS_PATH,
    "OFFERS_PATH": OFFERS_PATH,
    "UTILITY_PATH": UTILITY_PATH
})


def datetime_to_str(date: datetime) -> str:
    """Returns a datetime as string in the correct ISO format"""
    return date.isoformat(sep="T", timespec="seconds").split("+")[0]
