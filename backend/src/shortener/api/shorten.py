from typing import List, Optional

from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, Query, Body, Path, status, Response


from .. import schemas
from ..services.shorten import ShortenService
router = APIRouter(prefix='/shorten', tags=['Shorter'])


@router.post('/', response_model=schemas.Url, name='add new url', status_code=status.HTTP_201_CREATED)
def create_url(url_data: schemas.UrlCreate = Body(..., embed=True), service: ShortenService = Depends()):
    """
    ## Добавить новую ссылку
    - ***url***  - ссылка для сокращения, уникальная
    - ***user_short_link*** - пользовательская ссылка, уникальная
    \f
    :param url_data:
    :param service:
    :return:
    """
    return service.create(url_data=url_data)


@router.get('/', response_model=List[schemas.Url], name='get all urls data')
def get_all_urls(skip: Optional[int] = Query(0, ge=0), limit: Optional[int] = Query(100, gt=0),
                 service: ShortenService = Depends()):
    """
    ## Получить все данные нескольких ссылок по pk
    - ***skip*** первый элементы начиная с ***skip + 1***
    - ***limit*** количество элементов
    \f
    :param skip:
    :param limit:
    :param service:
    :return:
    """
    return service.get_all_urls(skip=skip, limit=limit)


@router.get('/url_data/', response_model=schemas.Url, name='get url data')
def get_url_data(short_link: str = Query(..., min_length=2, max_length=100), service: ShortenService = Depends()):
    """
    ## Получить данные одной ссылки
    - Возвращаются все данные ссылки
    - ***short_link*** автоматически сгенерированная ссылка (short link всегда ничанается с $)
     или пользовательская ссылка
    \f
    :param short_link:
    :param service:
    :return:
    """
    return service.get_url_data(short_link=short_link)


@router.get('/{short_link}/', name='get url', status_code=status.HTTP_301_MOVED_PERMANENTLY)
def get_url(short_link: str = Path(..., min_length=2, max_length=100), service: ShortenService = Depends()):
    """
    ## Перейти по сохраненному ранее короткому представлению и получить redirect на соответствующий исходный URL
    - Данные кешируются
    - ***short_link*** автоматически сгенирированная ссылка (short link всегда начинается с $)
     или пользовательская ссылка
     \f
    :param short_link:
    :param service:
    :return:
    """

    url = service.get_url(short_link=short_link)
    headers = {"Cache-Control": "private, max-age=60"}
    return RedirectResponse(url=url, status_code=status.HTTP_301_MOVED_PERMANENTLY, headers=headers)


@router.put('/url_data/{url_id}/', response_model=schemas.Url, name='edit url')
def edit_url(url_id: int = Path(..., gt=0), url_data: schemas.UrlEdit = Body(..., embed=True),
             service: ShortenService = Depends()):
    """
    # Редактировать данные ссылки
    - ***url_id*** - pk url
    - ***url***  - ссылка для сокращения, уникальная
    - ***user_short_link*** - пользовательская ссылка, уникальная
    \f
    :param url_id:
    :param url_data:
    :param service:
    :return:
    """
    return service.edit(url_id=url_id, url_data=url_data)


@router.delete('/url_data/{url_id}/', name='delete url', status_code=status.HTTP_204_NO_CONTENT)
def delete_url(url_id: int = Path(..., gt=0), service: ShortenService = Depends()):
    """
    ## Удалить ссылку
    - ***url_id*** - pk url
    \f
    :param url_id:
    :param service:
    :return:
    """
    service.delete(url_id=url_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
