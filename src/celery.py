import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery(__name__)

app.config_from_object(__name__, namespace="CELERY")

app.conf.broker_url = os.environ["CELERY_BROKER"]
app.conf.broker_transport_options = {"max_retries": 5}
app.conf.result_backend = "django-db"
app.conf.accept_content = ["pickle", "json"]
app.conf.timezone = "UTC"

app.conf.beat_schedule = {}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
