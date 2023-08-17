from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import orm

from src.database import Session, Base, engine
from src.main import app


@pytest.fixture(scope="session")
def session() -> Generator:
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()
    session = orm.Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
