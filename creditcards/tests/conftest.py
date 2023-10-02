import os
import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

os.environ['ENV'] = 'test'


def pytest_configure(config):
    env_file = find_dotenv('../.env.test')
    load_dotenv(env_file)
    return config


@pytest.fixture(scope="function")
def session(monkeypatch) -> Generator:
    """
    Sets up an alternate database connection, to a db_tests database.

    Args:
        monkeypatch: used to patch the SessionLocal variable in src.database

    Returns:
        SQLAlchemy session to the test database
    """
    from src import database
    from src.database import Base, SQLALCHEMY_DATABASE_URL

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        isolation_level="READ UNCOMMITTED"
    )
    session_local = sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False)

    monkeypatch.setattr(database, "SessionLocal", session_local)

    Base.metadata.create_all(bind=engine)
    sess = session_local(expire_on_commit=False)
    # begin a non-ORM transaction
    sess.begin()

    yield sess

    sess.rollback()
    sess.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    from src.main import app
    with TestClient(app) as c:
        yield c
