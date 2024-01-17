#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input

gunicorn --preload --bind 0.0.0.0:8000 src.asgi -w 4 -k uvicorn.workers.UvicornWorker