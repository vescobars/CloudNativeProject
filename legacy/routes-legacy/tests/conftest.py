from typing import Generator

import pytest
import requests
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import database
from src.constants import USERS_PATH
from src.database import Base, SQLALCHEMY_DATABASE_URL
from src.main import app


@pytest.fixture(scope="function")
def session(monkeypatch) -> Generator:
    """
    Sets up an alternate database connection, to a db_tests database.

    :param monkeypatch: used to patch the SessionLocal variable in src.database
    :return: SQLAlchemy session to the test database
    """

    test_db_url = SQLALCHEMY_DATABASE_URL
    print(test_db_url)
    engine = create_engine(
        test_db_url,
        isolation_level="READ UNCOMMITTED"
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False)

    monkeypatch.setattr(database, "SessionLocal", SessionLocal)

    Base.metadata.create_all(bind=engine)
    sess = SessionLocal(expire_on_commit=False)
    sess.begin()

    yield sess
    sess.rollback()
    sess.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def token(generate_test_user):
    user_id, user_profile = generate_test_user
    login_res = requests.post(f'{USERS_PATH}/users/auth', json={
        "username": user_profile["username"],
        "password": user_profile["password"],
    })
    assert login_res.status_code == 200, "Couldn't authenticate for a new token"
    print("Got new auth token")
    return login_res.json()["token"], user_id, user_profile


@pytest.fixture(scope="function")
def generate_test_user(faker) -> Generator:
    ping_res = requests.get(f'{USERS_PATH}/users/ping')
    assert ping_res.status_code == 200, "Can't find the /users microservice"
    faker.random.seed()
    profile = faker.simple_profile()
    payload = {
        "username": profile['username'],
        "password": faker.password(),
        "email": profile['mail'],
        "dni": faker.password(),
        "phoneNumber": faker.phone_number(),
        "fullName": profile['name']
    }

    create_res = requests.post(f'{USERS_PATH}/users/', json=payload)
    assert create_res.status_code == 201, "Couldn't create mock user"
    print("Created a new mock user")
    create_body = create_res.json()
    yield create_body['id'], payload
