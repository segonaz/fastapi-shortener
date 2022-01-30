
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

from .. settings import settings

engine = create_engine(settings.database_url)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)
redis_pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port,
                                  db=settings.redis_db, decode_responses=True)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


def get_redis_session():
    r = redis.Redis(connection_pool=redis_pool, charset='utf-8')
    try:
        yield r
    finally:
        pass


