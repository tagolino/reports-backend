from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Template, TemplateDataMapping, TemplateFile
from .serializers import (
    CreateTemplateSerializer,
    TemplateDetailsSerializer,
    TemplateListSerializer,
)
from .utils import add_template


class TemplateView(CreateAPIView, ListAPIView):
    queryset = Template.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TemplateListSerializer
        elif self.request.method == "POST":
            return CreateTemplateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template_name = request.data.get("name")
        template_type = request.data.get("type")
        template_file = request.data.get("file")
        template_is_active = request.data.get("is_active")
        template_file_expression = request.data.get("expression")
        response = add_template(template_file)

        if not response["success"]:
            template_file.close()

            if response["error"]:
                return Response(
                    response["error"], status=status.HTTP_400_BAD_REQUEST
                )

            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        template_id = response["data"]["templateId"]

        with transaction.atomic():
            new_template_object = Template.objects.create(
                name=template_name,
                type=template_type,
            )
            new_template_file = TemplateFile.objects.create(
                name=template_name,
                file=template_file,
                is_active=True if template_is_active == "true" else False,
                version=1,
                external_id=template_id,
                template=new_template_object,
            )
            TemplateDataMapping.objects.create(
                name="",
                mapping_expression=template_file_expression,
                template_file=new_template_file,
            )

        template_file.close()

        return Response(
            TemplateDetailsSerializer(new_template_object).data,
            status=status.HTTP_201_CREATED,
        )


class TemplateDetailsView(RetrieveAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateDetailsSerializer
