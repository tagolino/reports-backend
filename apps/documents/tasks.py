import carbone_sdk
from django.conf import settings
from django.core.files.base import ContentFile

from celery import shared_task

from .models import Document, DocumentGenerationRequest
from .utils import map_data


@shared_task
def process_document_generation_request(document_id):
    document = Document.objects.get(id=document_id)
    template_data_mapping = document.template_data_mapping
    mapping_expression = template_data_mapping.mapping_expression
    template_id = template_data_mapping.template_file.external_id
    csdk = carbone_sdk.CarboneSDK(settings.CARBONE_IO_API_TEST_TOKEN)

    for entry in document.generated_documents.all():
        data = map_data(entry.json_data, mapping_expression)
        json_data = {
            "data": data,
            "convertTo": "pdf",
            "lang": "en-gb",
        }

        try:
            report_bytes, _ = csdk.render(template_id, json_data)
        except Exception as err:
            entry.status = DocumentGenerationRequest.FAILED
            entry.error = err
            entry.save()

            continue

        try:
            entry.file.save(
                f"{document.name} ({entry.name}).pdf",
                ContentFile(report_bytes),
                save=True,
            )
        except Exception:
            continue

        entry.status = DocumentGenerationRequest.SUCCEEDED
        entry.save()
