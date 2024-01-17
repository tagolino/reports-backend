from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    # "loggers": {
    #     "django.db.backends": {
    #         "level": "DEBUG",
    #         "handlers": [
    #             "console",
    #         ],
    #     }
    # },
}
