from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField

from .enums import CurrencyEnum, ElectricityBillStatusEnum
from .managers import CustomerPortalManager


class CustomerPortalCountry(models.Model):
    country = CountryField()
    currency = models.CharField(choices=CurrencyEnum.choices, max_length=3)
    carbon_factor = models.DecimalField(
        max_digits=4, decimal_places=2, null=True
    )

    objects = CustomerPortalManager()

    class Meta:
        db_table = "countries"
        managed = False

    def __str__(self):
        return self.country.code


class CustomerPortalCustomer(models.Model):
    name = models.CharField(max_length=255)

    objects = CustomerPortalManager()

    class Meta:
        db_table = "customers"
        managed = False


class CustomerPortalAccountHolder(models.Model):
    name = models.CharField(max_length=255)
    customer = models.ForeignKey(
        CustomerPortalCustomer,
        on_delete=models.DO_NOTHING,
        related_name="account_holders",
    )

    objects = CustomerPortalManager()

    class Meta:
        db_table = "account_holders"
        managed = False

    def __str__(self):
        return self.name


class CustomerPortalAsset(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    region = models.ForeignKey(
        CustomerPortalCountry, on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = CustomerPortalManager()

    class Meta:
        db_table = "assets"
        managed = False

    def __str__(self):
        return self.name


class CustomerPortalECA(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        CustomerPortalCountry, on_delete=models.DO_NOTHING, null=True
    )

    account_holder = models.ForeignKey(
        CustomerPortalAccountHolder,
        on_delete=models.DO_NOTHING,
        related_name="electricity_customer_accounts",
    )

    objects = CustomerPortalManager()

    class Meta:
        db_table = "electricity_customer_accounts"
        managed = False


class CustomerPortalElectricityBill(models.Model):
    electricity_customer_account = models.ForeignKey(
        CustomerPortalECA,
        on_delete=models.DO_NOTHING,
        related_name="bills",
    )
    invoice_name = models.CharField(max_length=128, blank=True, default="")
    status = models.CharField(
        choices=ElectricityBillStatusEnum.choices,
        max_length=12,
        default=ElectricityBillStatusEnum.PAID_ON_TIME,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    payment_due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    objects = CustomerPortalManager()

    class Meta:
        db_table = "electricity_bills"
        managed = False

    def get_customer(self):
        return self.electricity_customer_account.account_holder.customer


class CustomerPortalMpan(models.Model):
    mpan = models.CharField(max_length=21, db_index=True, unique=True)
    electricity_customer_account = models.ForeignKey(
        CustomerPortalECA,
        on_delete=models.DO_NOTHING,
        related_name="active_mpans",
    )
    created_at = models.DateTimeField(default=timezone.now)

    objects = CustomerPortalManager()

    class Meta:
        db_table = "meters_mpan"
        managed = False

    def __str__(self):
        return self.mpan


class CustomerPortalMeterCompany(models.Model):
    name = models.CharField(max_length=255)

    objects = CustomerPortalManager()

    class Meta:
        db_table = "meter_companies"
        managed = False

    def __str__(self):
        return self.mpan


class CustomerPortalMeterDevice(models.Model):
    serial_number = models.CharField(max_length=32)
    company = models.ForeignKey(
        CustomerPortalMeterCompany,
        on_delete=models.CASCADE,
        related_name="meters",
    )

    objects = CustomerPortalManager()

    class Meta:
        db_table = "meter_devices"
        managed = False


class CustomerPortalMeter(models.Model):
    electricity_customer_account = models.ForeignKey(
        CustomerPortalECA,
        on_delete=models.DO_NOTHING,
        related_name="active_meters",
    )
    mpan = models.ForeignKey(
        CustomerPortalMpan, on_delete=models.DO_NOTHING, related_name="meters"
    )
    device = models.ForeignKey(
        CustomerPortalMeterDevice,
        on_delete=models.SET_NULL,
        related_name="meters",
        null=True,
        blank=True,
    )
    asset = models.ForeignKey(
        CustomerPortalAsset,
        on_delete=models.SET_NULL,
        related_name="meters",
        null=True,
        blank=True,
    )
    is_smart_meter = models.BooleanField()

    objects = CustomerPortalManager()

    class Meta:
        db_table = "meters"
        managed = False

    def __str__(self) -> str:
        return f"PK: {self.pk}; MPAN: {self.mpan}"


class CustomerPortalMeterConsumption(models.Model):
    meter = models.ForeignKey(
        CustomerPortalMeter,
        on_delete=models.DO_NOTHING,
        related_name="consumptions",
    )
    reading = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    consumption = models.DecimalField(
        default=0, max_digits=12, decimal_places=2
    )
    cost = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, null=True
    )
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    objects = CustomerPortalManager()

    class Meta:
        db_table = "meters_consumption_readings"
        managed = False


class CustomerPortalElectricitySupplier(models.Model):
    name = models.CharField(max_length=128)
    vat_number = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "electricity_suppliers"
        managed = False


class CustomerPortalElectricityContract(models.Model):
    name = models.CharField(max_length=255, null=True)
    account = models.ForeignKey(
        CustomerPortalECA,
        on_delete=models.DO_NOTHING,
        related_name="contracts",
    )
    supplier = models.ForeignKey(
        CustomerPortalElectricitySupplier,
        on_delete=models.DO_NOTHING,
        related_name="customer_contracts",
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    objects = CustomerPortalManager()

    class Meta:
        db_table = "electricity_customer_contracts"
        managed = False


class CustomerPortalElectricityBillMeter(models.Model):
    bill = models.ForeignKey(
        CustomerPortalElectricityBill, on_delete=models.DO_NOTHING
    )
    meter = models.ForeignKey(
        CustomerPortalMeter,
        on_delete=models.DO_NOTHING,
        related_name="meter_bills",
    )

    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    objects = CustomerPortalManager()

    class Meta:
        db_table = "electricity_bill_meters"
        managed = False

    def __str__(self) -> str:
        return "{}('{}','{}')".format(
            type(self).__name__, self.bill.pk, self.meter.mpan
        )
