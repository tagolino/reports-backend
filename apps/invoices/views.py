import logging
from collections import OrderedDict

from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Font
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import IndustryCharges, Invoice
from .serializers import InvoiceSerializer, InvoicesSerializer
from .utils import (
    INVOICE_EXCEL_COLUMNS,
    exclude_electricity_charges_fields,
    write_excel_row,
)

logger = logging.getLogger(__name__)


class InvoicesView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoicesSerializer


class InvoiceView(RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceExportXLSView(RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

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
        response[
            "Content-Disposition"
        ] = f"attachment; filename=invoice_{timezone.now():%Y%m%d%H%M%S}.xlsx"
        wb.save(response)

        return response
