from customers.serializers import (
    CustomerSerializer,
    ElectricityCustomerAccountSerializer,
)
from rest_framework import serializers

from .models import (
    BillingDetail,
    HHConsumptionCharges,
    IndustryCharges,
    Invoice,
    MeterInvoice,
    ReadingConsumptionCharges,
)


class BillingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetail
        fields = "__all__"


class HHConsumptionChargesSerializer(serializers.ModelSerializer):
    day_consumption_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    day_rate_value = serializers.DecimalField(max_digits=12, decimal_places=4)
    day_charges = serializers.DecimalField(max_digits=12, decimal_places=4)
    night_consumption_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    night_rate_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    night_charges = serializers.DecimalField(max_digits=12, decimal_places=4)
    total_electricity_charges = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )

    class Meta:
        model = HHConsumptionCharges
        fields = "__all__"


class IndustryChargesSerializer(serializers.ModelSerializer):
    quantity_1_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    quantity_2_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    rate_value = serializers.DecimalField(max_digits=12, decimal_places=4)
    charges = serializers.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        model = IndustryCharges
        fields = "__all__"


class ReadingConsumptionChargesSerializer(serializers.ModelSerializer):
    opening_reading = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    last_reading = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    consumption = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    rate = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    total_electricity_charges = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )

    class Meta:
        model = ReadingConsumptionCharges
        fields = "__all__"


class MeterInvoiceSerializer(serializers.ModelSerializer):
    customer_billing_details = BillingDetailSerializer()
    hh_consumption_charges = HHConsumptionChargesSerializer()
    industry_charges = serializers.SerializerMethodField()
    reading_consumption_charges = ReadingConsumptionChargesSerializer()
    levy_quantity = serializers.DecimalField(max_digits=12, decimal_places=4)
    levy_rate_value = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    levy_total = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    total_levies = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    total_no_vat = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    applicable_vat = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    charged_vat = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    bill_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    previous_balance = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    total_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=4,
    )

    class Meta:
        model = MeterInvoice
        fields = (
            "customer_billing_details",
            "hh_consumption_charges",
            "reading_consumption_charges",
            "industry_charges",
            "levy_name",
            "levy_quantity",
            "levy_unit",
            "levy_rate_value",
            "levy_rate_unit",
            "levy_total",
            "total_levies",
            "total_no_vat",
            "applicable_vat",
            "charged_vat",
            "bill_amount",
            "previous_balance",
            "total_amount",
        )

    def get_industry_charges(self, instance):
        if instance.industry_charges.exists():
            return IndustryChargesSerializer(
                instance.industry_charges.all(), many=True
            ).data


class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    electricity_customer_account = ElectricityCustomerAccountSerializer()
    meter_invoices = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = (
            "customer",
            "electricity_customer_account",
            "period_start_at",
            "period_end_at",
            "invoice_at",
            "meter_invoices",
        )

    def get_meter_invoices(self, instance):
        if instance.meter_invoices.exists():
            return MeterInvoiceSerializer(
                instance.meter_invoices.all(), many=True
            ).data


class InvoicesSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    electricity_customer_account = ElectricityCustomerAccountSerializer()

    class Meta:
        model = Invoice
        fields = (
            "customer",
            "electricity_customer_account",
            "period_start_at",
            "period_end_at",
            "invoice_at",
        )
