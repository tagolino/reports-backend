from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from templates.models import TemplateDataMapping

from .models import Document, DocumentDataFile, DocumentGenerationRequest
from .serializers import (
    CreateDocumentSerializer,
    DocumentDetailsSerializer,
    DocumentListSerializer,
)
from .tasks import process_document_generation_request
from .utils import get_file_json_content


class DocumentView(CreateAPIView, ListAPIView):
    queryset = Document.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DocumentListSerializer
        elif self.request.method == "POST":
            return CreateDocumentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document_name = request.data.get("name")
        data_file = request.data.get("data_file")
        template_id = request.data.get("template_id")
        is_production = request.data.get("is_production", False)
        template_data_mapping = TemplateDataMapping.objects.filter(
            template_file__template__id=template_id
        ).first()

        if not template_data_mapping:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            json_content = get_file_json_content(data_file)
        except Exception as e:
            return Response(
                e,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not json_content:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

        json_data = (
            json_content if isinstance(json_content, list) else [json_content]
        )

        with transaction.atomic():
            new_document_object = Document.objects.create(
                name=document_name,
                template_data_mapping=TemplateDataMapping.objects.filter(
                    template_file__template__id=template_id
                ).first(),
            )
            DocumentDataFile.objects.create(
                name=data_file.name,
                file=data_file,
                document=new_document_object,
            )

            for index in range(len(json_data)):
                DocumentGenerationRequest.objects.create(
                    name=f"{document_name} - {index + 1}",
                    document=new_document_object,
                    is_production=is_production,
                    json_data=json_data[index],
                )

        process_document_generation_request.delay(new_document_object.id)

        return Response(
            status=status.HTTP_201_CREATED,
        )


class DocumentDetailsView(RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentDetailsSerializer
