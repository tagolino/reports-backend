from django.db import models
from django_countries.fields import CountryField

from .enums import TemplateFileTypesEnum


class Country(models.Model):
    country = CountryField(blank_label="(select country)")

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.country.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)


class Template(models.Model):
    PROPOSAL = "PROPOSAL"
    INVOICE = "INVOICE"

    TYPE_CHOICES = (
        (PROPOSAL, "Proposal"),
        (INVOICE, "Invoice"),
    )

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(
        "templates.TemplateType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    sub_type = models.ForeignKey(
        "templates.TemplateSubType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True
    )


class TemplateFile(models.Model):
    ENGLISH = "ENGLISH"
    GERMAN = "GERMAN"

    LANGUAGE_CHOICES = (
        (ENGLISH, "English"),
        (GERMAN, "German"),
    )

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField()
    file = models.FileField(upload_to="template_files/%Y/%m/")
    file_type = models.CharField(
        choices=TemplateFileTypesEnum.choices,
        max_length=25,
        default=TemplateFileTypesEnum.PDF,
    )
    is_active = models.BooleanField(default=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=32)
    external_id = models.CharField(max_length=100, null=True, blank=True)
    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, related_name="template_files"
    )
    uploader = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True
    )


class TemplateDataMapping(models.Model):
    name = models.CharField(max_length=100)
    mapping_expression = models.JSONField(null=True, blank=True)
    template_file = models.ForeignKey(TemplateFile, on_delete=models.CASCADE)


class TemplateType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name if self.name else self.pk}"


class TemplateSubType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name if self.name else self.pk}"
