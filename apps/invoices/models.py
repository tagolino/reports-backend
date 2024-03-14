from customers.models import Customer, ElectricityCustomerAccount
from django.db import models
from documents.models import DataFileRequest


class HHConsumptionCharges(models.Model):
    day_consumption_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    day_consumption_unit = models.CharField(max_length=12)
    day_rate_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    day_rate_unit = models.CharField(max_length=12)
    day_charges = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    night_consumption_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    night_consumption_unit = models.CharField(max_length=12)
    night_rate_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    night_rate_unit = models.CharField(max_length=12)
    night_charges = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    total_electricity_charges = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "hh_consumption_charges"


class ReadingConsumptionCharges(models.Model):
    opening_reading = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    opening_reading_type = models.CharField(max_length=12)
    opening_reading_date = models.DateField()
    last_reading = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    last_reading_type = models.CharField(max_length=12)
    last_reading_date = models.DateField()
    consumption = models.DecimalField(
        default=0, max_digits=12, decimal_places=2
    )
    rate = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    total_electricity_charges = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "reading_consumption_charges"


class BillingDetail(models.Model):
    billing_name = models.CharField(max_length=255, blank=True, default="")
    billing_address_1 = models.CharField(max_length=255, blank=True, default="")
    billing_address_2 = models.CharField(max_length=255, blank=True, default="")
    billing_address_3 = models.CharField(max_length=255, blank=True, default="")
    billing_address_4 = models.CharField(max_length=255, blank=True, default="")
    billing_address_5 = models.CharField(max_length=255, blank=True, default="")
    billing_city = models.CharField(max_length=255, blank=True, default="")
    billing_postal_code = models.CharField(
        max_length=255, blank=True, default=""
    )
    site_name = models.CharField(max_length=255, blank=True, default="")
    site_address = models.CharField(max_length=255, blank=True, default="")
    vat_number = models.CharField(max_length=255, blank=True, default="")
    account_number = models.CharField(max_length=255, blank=True, default="")
    msn = models.CharField(max_length=32, blank=True, default="")
    pc = models.IntegerField(null=True)
    mtc = models.CharField(max_length=3, null=True)
    llf = models.CharField(max_length=3, null=True)
    mpan = models.CharField(
        max_length=21, db_index=True, blank=True, default=""
    )
    contract_end_at = models.DateTimeField()
    invoice_number = models.CharField(max_length=128, blank=True, default="")
    invoice_at = models.DateTimeField()
    bill_from_at = models.DateTimeField()
    bill_to_at = models.DateTimeField()
    payment_due_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "billing_details"

    def __str__(self) -> str:
        return (
            f"{self.invoice_number}: "
            f"{self.bill_from_at.date().isoformat()} - "
            f"{self.bill_from_at.date().isoformat()}"
        )


class Invoice(models.Model):
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL, related_name="invoices"
    )
    electricity_customer_account = models.ForeignKey(
        ElectricityCustomerAccount,
        null=True,
        on_delete=models.SET_NULL,
        related_name="invoices",
    )
    period_start_at = models.DateTimeField()
    period_end_at = models.DateTimeField()
    invoice_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoices"

    def __str__(self):
        return (
            f"{self.customer.name}"
            f" - {self.electricity_customer_account.name}"
            f" ({self.id})"
        )


class MeterInvoice(models.Model):
    data_file_request = models.ForeignKey(
        DataFileRequest,
        null=True,
        on_delete=models.SET_NULL,
        related_name="meter_invoices",
    )
    data_center_contract_meter_id = models.IntegerField(blank=True, null=True)
    customer_billing_details = models.OneToOneField(
        BillingDetail,
        null=True,
        on_delete=models.SET_NULL,
        related_name="meter_invoice",
    )
    hh_consumption_charges = models.ForeignKey(
        HHConsumptionCharges,
        null=True,
        on_delete=models.SET_NULL,
        related_name="meter_invoices",
    )
    reading_consumption_charges = models.ForeignKey(
        ReadingConsumptionCharges,
        null=True,
        on_delete=models.SET_NULL,
        related_name="meter_invoices",
    )
    levy_name = models.CharField(max_length=255, null=True)
    levy_quantity = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    levy_unit = models.CharField(max_length=12, null=True)
    levy_rate_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    levy_rate_unit = models.CharField(max_length=12)
    levy_total = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    total_levies = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    total_no_vat = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    applicable_vat = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    charged_vat = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    bill_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    previous_balance = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "meter_invoices"

    def __str__(self):
        return (
            (
                f"{self.customer_billing_details.billing_name}: "
                f"{self.customer_billing_details.invoice_number} - "
                f"{self.customer_billing_details.invoice_at.date().isoformat()}"
            )
            if self.customer_billing_details
            else f"{self.id}"
        )


class IndustryCharges(models.Model):
    name = models.CharField(max_length=255)
    meter_invoice = models.ForeignKey(
        MeterInvoice,
        null=True,
        on_delete=models.SET_NULL,
        related_name="industry_charges",
    )
    quantity_1_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    quantity_1_unit = models.CharField(max_length=12)
    quantity_2_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    quantity_2_unit = models.CharField(max_length=12)
    unit = models.CharField(max_length=12)
    rate_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    rate_unit = models.CharField(max_length=16)
    charges = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "industry_charges"
