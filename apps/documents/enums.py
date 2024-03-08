from django.db import models


class ActionTypesEnum(models.TextChoices):
    INVOICE = "INVOICE"
