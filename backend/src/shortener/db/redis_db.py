
from typing import Optional, Tuple

from fastapi import Depends
from redis import Redis

from . database import get_redis_session
from .. settings import settings


class RedisCache:
    def __init__(self,  redis_session: Redis = Depends(get_redis_session)):
        self.session = redis_session

    def get_url(self, key: str) -> Optional[str]:
        url = self.session.get(name=key)
        return url

    def set_url(self, keys: Tuple[str, Optional[str]], new_url: str) -> None:
        for key in filter(lambda x: x is not None, keys):
            self.session.set(name=key, value=new_url, ex=settings.redis_exat)

    def del_url(self, keys: Tuple[str, Optional[str]]) -> None:
        for key in filter(lambda x: x is not None, keys):
            self.session.delete(key)

    def edit_url(self, new_keys: Tuple[str, Optional[str]], old_key: str, new_url: str) -> None:
        self.del_url(keys=(old_key, None))
        self.set_url(keys=new_keys, new_url=new_url)
