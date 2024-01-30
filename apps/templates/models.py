from django.db import models
from django_countries.fields import CountryField


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
    type = models.CharField(choices=TYPE_CHOICES, max_length=32)
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
    mapping_expression = models.TextField(null=True, blank=True)
    template_file = models.ForeignKey(TemplateFile, on_delete=models.CASCADE)
