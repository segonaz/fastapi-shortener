from fastapi import FastAPI

from . import api


tags_metadata = [
    {
        'name': 'Shorter',
        'description': 'Создание, редактирование и получение ссылок.',
    }
]

app = FastAPI(
    title='Another shortener',
    description='Сервис для сокращения ссылок.',
    version='1.0.0',
    openapi_tags=tags_metadata
)

app.include_router(api.router)
