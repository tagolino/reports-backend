from django.db import models


class TemplateTypesEnum(models.TextChoices):
    PROPOSAL = "PROPOSAL"
    INVOICE = "INVOICE"


class TemplateSubTypesEnum(models.TextChoices):
    HH = "HH"
    NHH = "NHH"


class TemplateFileTypesEnum(models.TextChoices):
    PDF = "PDF"
    XLS = "XLS"
