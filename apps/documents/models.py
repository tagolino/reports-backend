from django.db import models
from templates.models import Template

from .enums import ActionTypesEnum


class Document(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_production = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    template_data_mapping = models.ForeignKey(
        "templates.TemplateDataMapping", on_delete=models.SET_NULL, null=True
    )
    created_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True
    )


class DocumentDataFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="data_files/%Y/%m/", null=True)
    data_file_request = models.ForeignKey(
        "documents.DataFileRequest",
        null=True,
        on_delete=models.SET_NULL,
        related_name="data_documents",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="data_documents"
    )


class DocumentGenerationRequest(models.Model):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (SUCCEEDED, "Succeeded"),
        (FAILED, "Failed"),
    )

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/%Y/%m/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=32, default=PENDING
    )
    error = models.TextField()
    json_data = models.JSONField(null=True, default=None)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="generated_documents"
    )


class DataFileRequest(models.Model):
    action_type = models.CharField(
        choices=ActionTypesEnum.choices,
        max_length=45,
        default=ActionTypesEnum.INVOICE,
    )
    name = models.CharField(max_length=225)
    document_template = models.ForeignKey(
        Template,
        null=True,
        on_delete=models.SET_NULL,
        related_name="data_file_requests",
    )
    customers = models.JSONField(null=True)
    contracts = models.JSONField(null=True)
    account_holders = models.JSONField(null=True)
    electricity_customer_accounts = models.JSONField(null=True)
    sites = models.JSONField(null=True)
    mpans = models.JSONField(null=True)

    period_start_at = models.DateField()
    period_end_at = models.DateField()

    xls_file = models.FileField(upload_to="data_file/%Y/%m/", null=True)

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="data_file_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "data_file_requests"

    def __str__(self):
        return (
            f"{self.action_type}"
            f" {self.created_at:%Y%m%d_%H%M%S}"
            f" ({self.id})"
        )
