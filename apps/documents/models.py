from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    template_data_mapping = models.ForeignKey(
        "templates.TemplateDataMapping", on_delete=models.SET_NULL, null=True
    )


class DocumentDataFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="data_files/%Y/%m/")
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
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
