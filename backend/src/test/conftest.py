from os import environ

import pytest
from fastapi.testclient import TestClient


# Устанавливаем `os.environ`, прежде чем загружаем наше приложение чтобы использовать тестовую БД.
# ignore PEP8
environ['IS_TEST'] = 'True'

from ..shortener.main import app         # noqa
from ..shortener.db import Base, engine, get_redis_session # noqa


@pytest.fixture(scope='module')
def test_app():
    # Clear data in tests databases
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    redis_db = next(get_redis_session())
    redis_db.flushdb()

    client = TestClient(app)
    yield client
