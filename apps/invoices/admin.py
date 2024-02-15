from django.contrib import admin

from .models import (
    BillingDetail,
    HHConsumptionCharges,
    IndustryCharges,
    Invoice,
    MeterInvoice,
    ReadingConsumptionCharges,
)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "electricity_customer_account",
        "period_start_at",
        "period_end_at",
        "invoice_at",
    ]


@admin.register(BillingDetail)
class BillingDetailsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "invoice_number",
        "invoice_at",
        "bill_from_at",
        "bill_to_at",
        "payment_due_at",
    ]


@admin.register(MeterInvoice)
class MeterInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "invoice",
        "customer_billing_details",
    ]


@admin.register(HHConsumptionCharges)
class HHConsumptionChargesAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "total_electricity_charges",
    ]


@admin.register(ReadingConsumptionCharges)
class ReadingConsumptionChargesAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "opening_reading_date",
        "opening_reading",
        "last_reading_date",
        "last_reading",
        "consumption",
        "rate",
        "total_electricity_charges",
    ]


@admin.register(IndustryCharges)
class IndustryChargesAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "meter_invoice",
        "created_at",
    ]
