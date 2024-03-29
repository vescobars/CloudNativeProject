from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import database
from src.database import Base, SQLALCHEMY_DATABASE_URL
from src.main import app


@pytest.fixture(scope="function")
def session(monkeypatch) -> Generator:
    """
    Sets up an alternate database connection, to a db_tests database.

    Args:
        monkeypatch: used to patch the SessionLocal variable in src.database

    Returns:
        SQLAlchemy session to the test database
    """
    test_db_url = SQLALCHEMY_DATABASE_URL + "_tests"

    engine = create_engine(
        test_db_url,
        isolation_level="READ UNCOMMITTED"
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False)

    monkeypatch.setattr(database, "SessionLocal", SessionLocal)

    Base.metadata.create_all(bind=engine)
    sess = SessionLocal(expire_on_commit=False)
    # begin a non-ORM transaction
    sess.begin()

    yield sess

    sess.rollback()
    sess.close()


# @pytest.fixture(scope=any_non_session_scope, autouse=True)
# def faker_seed():
#     return 12345


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
