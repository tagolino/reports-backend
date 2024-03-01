from collections import OrderedDict

from django.http import HttpResponse
from django.utils import timezone
from invoices.models import IndustryCharges
from invoices.utils import (
    INVOICE_EXCEL_COLUMNS,
    exclude_electricity_charges_fields,
    write_excel_row,
)
from openpyxl import Workbook
from openpyxl.styles import Font
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from .enums import ActionTypesEnum
from .filters import DataFileRequestFilter, DocumentFilter
from .models import DataFileRequest, Document
from .serializers import (
    CreateDocumentSerializer,
    DataFileRequestDetailSerializer,
    DataFileRequestSerializer,
    DocumentDetailsSerializer,
    DocumentListSerializer,
)
from .tasks import process_data_file, process_document_generation_request


class DocumentView(ListCreateAPIView):
    queryset = Document.objects.prefetch_related(
        "template_data_mapping__template_file__template"
    ).all()
    filterset_class = DocumentFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DocumentListSerializer
        elif self.request.method == "POST":
            return CreateDocumentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        process_document_generation_request.delay(instance.id)
        return Response(
            DocumentDetailsSerializer(instance).data, status.HTTP_201_CREATED
        )


class DocumentDetailsView(RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentDetailsSerializer


class DataFileRequestView(ListCreateAPIView):
    queryset = DataFileRequest.objects.all()
    filterset_class = DataFileRequestFilter
    serializer_class = DataFileRequestSerializer

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        if instance.action_type == ActionTypesEnum.INVOICE:
            process_data_file.delay(instance.id)


class DataFileRequestDetailView(
    RetrieveAPIView,
):
    queryset = DataFileRequest.objects.all()
    serializer_class = DataFileRequestDetailSerializer


class DataFileXLSExportView(RetrieveAPIView):
    queryset = DataFileRequest.objects.all()
    serializer_class = DataFileRequestDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        row_number = 1

        headers = exclude_electricity_charges_fields(
            INVOICE_EXCEL_COLUMNS,
            request.query_params.get("electricity_charges", "hh"),
        )

        for index, header in enumerate(headers):
            ws.cell(row=row_number, column=index + 1, value=header).font = Font(
                bold=True
            )
        row_number += 1

        instance = self.get_object()
        data = self.get_serializer(instance).data
        columns = list(headers.values())

        for index, meter_invoice in enumerate(data["meter_invoices"]):
            write_excel_row(ws, row_number, columns, meter_invoice)
            for related_field in [
                "customer_billing_details",
                "hh_consumption_charges",
                "reading_consumption_charges",
            ]:
                if meter_invoice.get(related_field):
                    write_excel_row(
                        ws,
                        row_number,
                        columns,
                        meter_invoice[related_field],
                    )

            if meter_invoice.get("industry_charges"):
                data = OrderedDict()
                total_industry_charges = 0
                for index, industry_charge in enumerate(
                    meter_invoice["industry_charges"]
                ):
                    for field in IndustryCharges._meta.fields:
                        field_value = ""
                        if industry_charge.get(field.name) is not None:
                            field_value = industry_charge[field.name]

                            if field.name == "charges" and industry_charge.get(
                                field.name
                            ):
                                total_industry_charges += float(
                                    industry_charge[field.name]
                                )
                        data[
                            f"industry_charge_{index + 1}_{field.name}"
                        ] = field_value
                data["total_industry_charges"] = total_industry_charges
                write_excel_row(
                    ws,
                    row_number,
                    columns,
                    data,
                )

            row_number += 1

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f"attachment; filename={instance.action_type.title()}"
            f" {timezone.now():%Y%m%d_%H%M%S}.xlsx"
        )
        wb.save(response)

        return response
