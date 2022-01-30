from datetime import datetime
from pydantic import BaseModel, AnyUrl, Field, validator
from typing import Optional


class BaseUrl(BaseModel):
    url: AnyUrl = Field(..., description='Url', example='https://www.google.com/')
    user_short_link: Optional[str] = Field(None, description='User short link', example='my link')


class Url(BaseUrl):
    id: int = Field(..., gt=0, example=6)
    id_hash: str = Field(..., alias='short link', description='Short link for url', example='$g')
    url_hash: str = Field(..., description='Hashed url', example='d75277cdffef995a46ae59bdaef1db86')
    user_link_hash: Optional[str] = Field(None, description='Hashed user shor link')
    created_at: datetime = Field(..., description='Created at')

    class Config:
        orm_mode = True,
        allow_population_by_field_name = True


class UrlCreate(BaseUrl):

    @validator('user_short_link')
    def user_shor_link_validation(cls, user_short_link: str) -> Optional[str]:
        if user_short_link is not None and (user_short_link.startswith('url_data') or user_short_link.startswith('$')):
            raise ValueError(f'Invalid user short link value: {user_short_link}')
        return user_short_link


class UrlEdit(UrlCreate):
    pass


class ViewUrl(BaseModel):
    url: AnyUrl = Field(..., description='Url', example='https://www.google.com/')
