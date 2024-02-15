from invoices.models import Invoice
from invoices.tasks import create_customer_invoice
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import CustomerInvoiceSerializer


class CustomerInvoiceView(CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = CustomerInvoiceSerializer

    def create(self, request, *args, **kwargs):
        try:
            instance = Invoice.objects.get(
                customer_id=request.data.get("customer"),
                invoice_at=request.data.get("invoice_at"),
            )
        except Invoice.DoesNotExist:
            serializer = self.get_serializer(
                data={"customer": kwargs["pk"], **request.data}
            )
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

        create_customer_invoice.delay(instance.id)

        return Response(
            status=status.HTTP_201_CREATED,
        )
