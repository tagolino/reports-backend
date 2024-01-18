import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = [
    "*",
]

CSRF_TRUSTED_ORIGINS = [
    "https://reports-backend.dgtlpower.com",
    "http://reports-backend.dgtlpower.com",
]

if os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[
            DjangoIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
