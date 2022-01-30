from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Url(Base):
    __tablename__ = 'url'

    id = Column(Integer, primary_key=True)
    id_hash = Column(String(20), index=True)
    url = Column(String, nullable=False)
    url_hash = Column(String(32), index=True, unique=True, nullable=False)
    user_short_link = Column(String, nullable=True)
    user_link_hash = Column(String(10), index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
