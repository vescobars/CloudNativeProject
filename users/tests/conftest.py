from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event, orm
from sqlalchemy.orm import scoped_session

from src.database import SessionLocal, Base, engine
from src.main import app


@pytest.fixture(scope="function")
def session() -> Generator:
    Base.metadata.create_all(bind=engine)
    sess = SessionLocal(expire_on_commit=False)
    # begin a non-ORM transaction
    savepoint = sess.begin_nested()

    yield sess

    sess.rollback()
    sess.close()

@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
