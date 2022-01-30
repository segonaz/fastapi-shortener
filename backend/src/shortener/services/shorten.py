
from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. settings import settings
from .. services import utils
from ..db.database import get_session
from ..db.redis_db import RedisCache
from ..db import models
from .. import schemas


class ShortenService:
    def __init__(self, session: Session = Depends(get_session), cache: RedisCache = Depends()):
        self.session = session
        self.cache = cache

    def get_all_urls(self, skip: int = 0, limit: int = 100) -> List[models.Url]:
        urls = self.session.query(models.Url).offset(skip).limit(limit).all()
        if not urls:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return urls

    def get_url(self, short_link) -> Optional[str]:
        url = self.cache.get_url(key=short_link)
        if url:
            return url
        # no data in cache, lets check db
        if short_link[0] == settings.url_prefix:
            url_id = utils.decode(short_link, settings.alphabet)
            if url_id is not None:
                url = self.session.query(models.Url.url).filter(models.Url.id == url_id).first()
        else:
            user_link_hash = utils.get_hash(short_link)[-settings.user_link_hash_length:]
            url = self.session.query(models.Url.url).filter(models.Url.user_link_hash == user_link_hash).first()
        if not url:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        self.cache.set_url(keys=(short_link, None), new_url=url.url) # noqa
        return url.url                                               # noqa

    def get_url_data(self, short_link) -> Optional[models.Url]:
        if short_link[0] == settings.url_prefix:
            url = self._get_url_by_hash_id(id_hash=short_link)
        else:
            user_link_hash = utils.get_hash(short_link)[-settings.user_link_hash_length:]
            url = self._get_url_by_user_link(user_link_hash=user_link_hash)
        if not url:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return url

    def create(self, url_data: schemas.UrlCreate) -> Optional[models.Url]:
        user_link_hash = None
        url_hash = utils.get_hash(url_data.url.strip('/'))

        if self.session.query(models.Url.id).filter(models.Url.url_hash == url_hash).first():
            raise HTTPException(status_code=400, detail='Url already exist')

        if url_data.user_short_link:
            user_link_hash = utils.get_hash(url_data.user_short_link)[-settings.user_link_hash_length:]
            if self._get_url_by_user_link(user_link_hash=user_link_hash):
                raise HTTPException(status_code=400, detail='User short link already exist')
        new_url = models.Url(url=url_data.url, url_hash=url_hash,
                             user_short_link=url_data.user_short_link, user_link_hash=user_link_hash)

        self.session.add(new_url)
        self.session.commit()
        self.session.refresh(new_url)
        new_url.id_hash = utils.encode(new_url.id, settings.alphabet)
        self.session.commit()
        # Add new url in cache
        self.cache.set_url(keys=(new_url.id_hash, new_url.user_short_link), new_url=new_url.url)
        return new_url

    def edit(self, url_id: int, url_data: schemas.UrlCreate) -> Optional[models.Url]:
        edit_url = self._get_by_id(url_id)
        old_user_link = edit_url.user_short_link
        url_hash = utils.get_hash(url_data.url.strip('/'))

        if self.session.query(models.Url.id).\
                filter(models.Url.url_hash == url_hash, models.Url.id != edit_url.id).first():
            raise HTTPException(status_code=400, detail='Url already exist')

        if url_data.user_short_link:
            user_link_hash = utils.get_hash(url_data.user_short_link)[-settings.user_link_hash_length:]
            if self.session.query(models.Url.id).\
                    filter(models.Url.user_link_hash == user_link_hash, models.Url.id != edit_url.id).first():
                raise HTTPException(status_code=400, detail='User short link already exist')
            edit_url.user_short_link = url_data.user_short_link
            edit_url.user_link_hash = user_link_hash

        edit_url.url = url_data.url
        edit_url.url_hash = url_hash

        self.session.add(edit_url)
        self.session.commit()
        self.session.refresh(edit_url)
        # Edit cache data
        self.cache.edit_url(new_keys=(edit_url.id_hash, edit_url.user_short_link),
                            old_key=old_user_link, new_url=edit_url.url)
        return edit_url

    def delete(self, url_id: int) -> None:
        url_for_delete = self._get_by_id(url_id)

        self.session.delete(url_for_delete)
        self.session.commit()
        self.cache.del_url(keys=(url_for_delete.user_short_link, url_for_delete.id_hash))
        return

    def _get_url_by_hash_id(self, id_hash: str) -> Optional[models.Url]:
        url_id = utils.decode(id_hash, settings.alphabet)
        if url_id is None:
            return
        url = self.session.query(models.Url).filter(models.Url.id == url_id).first()
        return url

    def _get_url_by_user_link(self, user_link_hash) -> Optional[models.Url]:
        return self.session.query(models.Url).filter(models.Url.user_link_hash == user_link_hash).first()

    def _get_by_id(self, url_id: int) -> Optional[models.Url]:
        url = self.session.query(models.Url).filter(models.Url.id == url_id).first()
        if not url:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return url
