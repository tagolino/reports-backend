from django.db import models


class CurrencyEnum(models.TextChoices):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class ElectricityBillStatusEnum(models.TextChoices):
    OVERDUE = "OVERDUE"
    PENDING = "PENDING"
    PAID_ON_TIME = "PAID_ON_TIME"
