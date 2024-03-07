from invoices.models import Invoice
from rest_framework import serializers

from .models import Customer, ElectricityCustomerAccount


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "name")


class ElectricityCustomerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityCustomerAccount
        fields = ("id", "name")


class CustomerInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            "customer",
            "electricity_customer_account",
            "period_start_at",
            "period_end_at",
            "invoice_at",
        )
