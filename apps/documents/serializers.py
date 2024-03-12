from collections import OrderedDict

from django.db import transaction
from invoices.models import IndustryCharges
from invoices.serializers import MeterInvoiceSerializer
from invoices.utils import INVOICE_EXCEL_COLUMNS, get_mapped_json_data
from rest_framework import serializers
from templates.models import TemplateDataMapping
from templates.serializers import TemplateDetailsSerializer
from users.serializers import CreatedBySerializer

from .models import (
    DataFileRequest,
    Document,
    DocumentDataFile,
    DocumentGenerationRequest,
)
from .utils import get_file_json_content


class DynamicFieldsSerializerMixin:
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DocumentDataFileSerializer(
    DynamicFieldsSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = DocumentDataFile
        fields = (
            "name",
            "created_at",
            "file",
        )


class DocumentListSerializer(serializers.ModelSerializer):
    template = serializers.SerializerMethodField()
    data_file = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ("id", "name", "created_at", "template", "data_file")

    def get_template(self, instance):
        try:
            template = instance.template_data_mapping.template_file.template

            return TemplateDetailsSerializer(
                template, fields=["id", "name"]
            ).data
        except KeyError:
            return None

    def get_data_file(self, instance):
        try:
            last_data_file = instance.data_documents.last()

            return DocumentDataFileSerializer(
                last_data_file, fields=["name", "file"]
            ).data
        except KeyError:
            return None


class DataFileRequestDetailSerializer(serializers.ModelSerializer):
    meter_invoices = MeterInvoiceSerializer(many=True)

    class Meta:
        model = DataFileRequest
        fields = "__all__"


class CreateDocumentSerializer(serializers.Serializer):
    name = serializers.CharField()
    template_id = serializers.IntegerField()
    is_production = serializers.BooleanField()

    def validate(self, attrs):
        data = self.context["request"].data
        if (
            data.get("data_file") is None or data.get("data_file") == "null"
        ) and (
            data.get("data_file_id") is None or data.get("data_file_id") == ""
        ):
            raise serializers.ValidationError(
                {"data_file": "No data file found."}
            )
        return super().validate(attrs)

    def create(self, validated_data):
        data_file = self.initial_data["data_file"]
        data_file_id = self.initial_data["data_file_id"]
        document_name = validated_data["name"]
        template_id = validated_data["template_id"]
        is_production = validated_data["is_production"]

        try:
            template_data_mapping = TemplateDataMapping.objects.get(
                template_file__template__id=template_id
            )
        except TemplateDataMapping.DoesNotExist:
            raise serializers.ValidationError(
                "Template data mapping not found."
            )

        if data_file_id:
            json_data = []
            try:
                data_file_request = DataFileRequest.objects.get(id=data_file_id)
            except DataFileRequest.DoesNotExist:
                raise serializers.ValidationError(
                    "Data file request not found."
                )

            data_file_record = DataFileRequestDetailSerializer(
                data_file_request
            ).data

            for meter_invoice in data_file_record["meter_invoices"]:
                json_datum = get_mapped_json_data(
                    {}, INVOICE_EXCEL_COLUMNS, meter_invoice
                )
                for related_field in [
                    "customer_billing_details",
                    "hh_consumption_charges",
                    "reading_consumption_charges",
                ]:
                    if meter_invoice.get(related_field):
                        json_datum = get_mapped_json_data(
                            json_datum,
                            INVOICE_EXCEL_COLUMNS,
                            meter_invoice[related_field],
                        )

                if meter_invoice.get("industry_charges"):
                    industry_charges_datum = OrderedDict()
                    total_industry_charges = 0
                    for index, industry_charge in enumerate(
                        meter_invoice["industry_charges"]
                    ):
                        for field in IndustryCharges._meta.fields:
                            field_value = ""
                            if industry_charge.get(field.name) is not None:
                                field_value = industry_charge[field.name]

                                if (
                                    field.name == "charges"
                                    and industry_charge.get(field.name)
                                ):
                                    total_industry_charges += float(
                                        industry_charge[field.name]
                                    )
                            industry_charges_datum[
                                f"industry_charge_{index + 1}_{field.name}"
                            ] = field_value
                    industry_charges_datum[
                        "total_industry_charges"
                    ] = total_industry_charges
                    json_datum = get_mapped_json_data(
                        json_datum,
                        INVOICE_EXCEL_COLUMNS,
                        industry_charges_datum,
                    )
                json_data.append(json_datum)
        else:
            try:
                json_content = get_file_json_content(data_file)
            except Exception:
                raise serializers.ValidationError(
                    "Extracting data file JSON failed."
                )

            if not json_content:
                raise serializers.ValidationError(
                    "Uploaded data file is invalid."
                )

            json_data = (
                json_content
                if isinstance(json_content, list)
                else [json_content]
            )

        with transaction.atomic():
            new_document_object = Document.objects.create(
                name=document_name,
                template_data_mapping=template_data_mapping,
            )

            if data_file_id:
                DocumentDataFile.objects.create(
                    name=data_file_request.name,
                    data_file_request=data_file_request,
                    document=new_document_object,
                )
            else:
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

        return new_document_object


class DocumentGenerationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentGenerationRequest
        fields = (
            "name",
            "created_at",
            "status",
            "error",
            "file",
        )


class DocumentDetailsSerializer(serializers.ModelSerializer):
    data_documents = DocumentDataFileSerializer(many=True)
    generated_documents = DocumentGenerationRequestSerializer(many=True)

    class Meta:
        model = Document
        fields = (
            "id",
            "name",
            "created_at",
            "data_documents",
            "generated_documents",
        )


class DataFileRequestSerializer(serializers.ModelSerializer):
    created_by = CreatedBySerializer(read_only=True)

    class Meta:
        model = DataFileRequest
        fields = "__all__"
