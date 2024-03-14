from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import (
    Supplier,
    Template,
    TemplateDataMapping,
    TemplateFile,
    TemplateType,
)
from .serializers import (
    CreateTemplateSerializer,
    SupplierListSerializer,
    TemplateDetailsSerializer,
    TemplateListSerializer,
    TemplateTypeListSerializer,
)
from .utils import add_template


class SupplierView(ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierListSerializer


class TemplateTypeView(ListAPIView):
    queryset = TemplateType.objects.all()
    serializer_class = TemplateTypeListSerializer
    pagination_class = None


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
        template_sub_type = request.data.get("sub_type")
        template_file = request.data.get("file")
        template_is_active = request.data.get("is_active")
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
            template_type_object = TemplateType.objects.get(id=template_type)
            new_template_object = Template.objects.create(
                name=template_name,
                type=template_type_object,
                sub_type=template_sub_type,
            )
            new_template_file = TemplateFile.objects.create(
                name=template_name,
                file=template_file,
                is_active=True if template_is_active == "true" else False,
                version=1,
                external_id=template_id,
                template=new_template_object,
                uploader=request.user,
            )
            TemplateDataMapping.objects.create(
                name="One to one mapping",
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
