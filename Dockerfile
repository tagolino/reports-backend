FROM python:3.11

# Sets an environmental variable that ensures output from python is sent straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv

RUN pipenv install --deploy --system

COPY . /app/

RUN yes | apt-get update
RUN yes | apt-get install nano gdal-bin libgdal-dev libmagic1

CMD gunicorn --preload --bind 0.0.0.0:8000 src.asgi -w 4 -k uvicorn.workers.UvicornWorker
