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
DB_PORT = os.environ.get("DB_PORT", "13001")
DB_NAME = os.environ.get("DB_NAME", "db")
USERS_PATH = os.environ.get("USERS_PATH", "http://localhost:3000")
TRUENATIVE_PATH = os.environ.get("TRUENATIVE_PATH", "http://localhost:3000")
SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "secrettoken")
SECRET_FAAS_TOKEN = os.environ.get("SECRET_FAAS_TOKEN", "secret_faas_token")
POLLING_PATH = os.environ.get("POLLING_PATH",
                              "https://us-central1-miso-grupo-17.cloudfunctions.net/card_status_polling")


def datetime_to_str(date: datetime) -> str:
    """Returns a datetime as string in the correct ISO format"""
    return date.isoformat(sep="T", timespec="seconds").split("+")[0]
