import os
from typing import Generator

import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient

os.environ['ENV'] = 'test'


def pytest_configure(config):
    env_file = find_dotenv('../.env.test')
    load_dotenv(env_file)
    return config


@pytest.fixture(scope="module")
def client() -> Generator:
    from src.main import app
    with TestClient(app) as c:
        yield c
