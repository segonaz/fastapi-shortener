FROM tiangolo/uvicorn-gunicorn:python3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PYTHONPATH /backend

ENV PORT 8000
ENV MODULE_NAME src.shortener.main
ENV VARIABLE_NAME app
ENV PRE_START_PATH /backend/scripts/prestart.sh

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY ./src /backend/src
COPY ./scripts /backend/scripts
COPY ./.env.example /backend/.env.example
