from django.db import models
from django_countries.fields import CountryField

from .managers import BillingServiceManager


class BillingServiceCustomer(models.Model):
    name = models.CharField(max_length=255)
    customer_portal_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    objects = BillingServiceManager()

    class Meta:
        db_table = "customers"
        managed = False

    def __str__(self) -> str:
        return self.name


class BillingServiceElectricityCustomerAccount(models.Model):
    name = models.CharField(max_length=255)
    country = CountryField(null=True, blank=True)
    billing_cycle = models.CharField()
    customer = models.ForeignKey(
        BillingServiceCustomer,
        on_delete=models.DO_NOTHING,
        related_name="electricity_customer_accounts",
    )
    customer_portal_id = models.IntegerField()
    billing_name = models.CharField(max_length=255, blank=True)
    billing_address_1 = models.CharField(max_length=255, blank=True)
    billing_address_2 = models.CharField(max_length=255, blank=True)
    billing_address_3 = models.CharField(max_length=255, blank=True)
    billing_address_4 = models.CharField(max_length=255, blank=True)
    billing_address_5 = models.CharField(max_length=255, blank=True)
    billing_city = models.CharField(max_length=255, blank=True)
    billing_postal_code = models.CharField(max_length=36, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = BillingServiceManager()

    class Meta:
        db_table = "electricity_customer_accounts"
        managed = False

    def __str__(self) -> str:
        return self.name


class BillingServiceMPAN(models.Model):
    mpan = models.CharField(max_length=21)
    customer_portal_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = BillingServiceManager()

    class Meta:
        db_table = "mpans"
        managed = False

    def __str__(self) -> str:
        return self.mpan


class BillingServiceMeter(models.Model):
    electricity_customer_account = models.ForeignKey(
        BillingServiceElectricityCustomerAccount,
        on_delete=models.DO_NOTHING,
        related_name="meters",
    )
    mpan = models.ForeignKey(
        BillingServiceMPAN,
        on_delete=models.DO_NOTHING,
        related_name="meters",
        null=True,
        blank=True,
    )
    serial_number = models.CharField(max_length=64)
    site_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    is_smart_meter = models.BooleanField()
    customer_portal_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = BillingServiceManager()

    class Meta:
        db_table = "meters"
        managed = False

    def __str__(self) -> str:
        return (
            f"MPAN: {getattr(self.mpan, 'mpan', '-')}, SN: {self.serial_number}"
        )


class BillingServiceElectricityCustomerAccountMeter(models.Model):
    electricity_customer_account = models.ForeignKey(
        BillingServiceElectricityCustomerAccount, on_delete=models.DO_NOTHING
    )
    meter = models.ForeignKey(
        BillingServiceMeter,
        on_delete=models.DO_NOTHING,
        related_name="electricity_customer_account_meters",
    )
    connected_at = models.DateTimeField()
    disconnected_at = models.DateTimeField()

    objects = BillingServiceManager()

    class Meta:
        db_table = "electricity_customer_account_meters"
        managed = False

    def __str__(self) -> str:
        return "{}('{}','{}','{}')".format(
            type(self).__name__,
            self.electricity_customer_account.name,
            self.meter.mpan,
            self.connected_at.strftime("%Y-%m-%d %H:%M:%S"),
        )


class BillingServiceContract(models.Model):
    account = models.ForeignKey(
        BillingServiceElectricityCustomerAccount,
        on_delete=models.DO_NOTHING,
        related_name="contracts",
    )

    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)
    vat_number = models.CharField(max_length=64)
    vat = models.DecimalField(max_digits=5, decimal_places=2)

    plan_type = models.CharField(max_length=24)

    night_time_start = models.TimeField()
    night_time_end = models.TimeField()

    payment_terms_due_date = models.IntegerField()

    customer_portal_id = models.IntegerField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = BillingServiceManager()

    class Meta:
        db_table = "contracts"
        managed = False

    def __str__(self) -> str:
        return self.name


class BillingServiceContractMeter(models.Model):
    contract = models.ForeignKey(
        BillingServiceContract,
        on_delete=models.DO_NOTHING,
        related_name="meters",
    )
    meter = models.ForeignKey(
        BillingServiceMeter,
        on_delete=models.DO_NOTHING,
        related_name="contracts",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    standing_charge = models.DecimalField(max_digits=12, decimal_places=4)
    day_unit_rate = models.DecimalField(max_digits=12, decimal_places=4)
    night_unit_rate = models.DecimalField(max_digits=12, decimal_places=4)
    ewe_unit_rate = models.DecimalField(max_digits=12, decimal_places=4)
    daily_capacity = models.DecimalField(max_digits=12, decimal_places=4)
    capacity = models.DecimalField(max_digits=12, decimal_places=4)
    total_eac = models.DecimalField(max_digits=12, decimal_places=4)
    excess_capacity_charge = models.DecimalField(
        max_digits=12, decimal_places=4
    )
    reactive_charge = models.DecimalField(max_digits=12, decimal_places=4)
    distribution_charge = models.DecimalField(max_digits=12, decimal_places=4)
    transmission_charge = models.DecimalField(max_digits=12, decimal_places=4)
    climate_change_levy = models.DecimalField(max_digits=12, decimal_places=4)
    mop_hh = models.DecimalField(max_digits=12, decimal_places=4)
    da_dc_hh = models.DecimalField(max_digits=12, decimal_places=4)

    objects = BillingServiceManager()

    class Meta:
        db_table = "contracts_meters"
        managed = False

    def __str__(self):
        return f"""
            Contract: {self.contract.name},
            Start-date: {self.start_date},
            End-date: {self.end_date}"
        """
