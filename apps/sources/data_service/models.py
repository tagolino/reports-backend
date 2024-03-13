from django.db import models

from .managers import DataServiceManager


class DataServiceCustomer(models.Model):
    name = models.CharField(max_length=255)

    customer_portal_id = models.IntegerField(blank=True, null=True)

    objects = DataServiceManager()

    class Meta:
        db_table = "customers"
        managed = False

    def __str__(self) -> str:
        return self.name


class DataServiceContract(models.Model):
    customer = models.ForeignKey(
        DataServiceCustomer,
        on_delete=models.DO_NOTHING,
        related_name="contracts",
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    vat = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    customer_portal_id = models.IntegerField(blank=True, null=True)

    objects = DataServiceManager()

    class Meta:
        db_table = "contracts"
        managed = False

    def __str__(self) -> str:
        return f"{self.name if self.name else self.pk}"


class DataServiceMPAN(models.Model):
    mpan = models.CharField(max_length=21, db_index=True, unique=True)

    mtc = models.CharField(max_length=3, null=True)
    pc = models.IntegerField()
    llfc = models.CharField(max_length=3, null=True)

    objects = DataServiceManager()

    class Meta:
        db_table = "mpans"
        managed = False

    def __str__(self) -> str:
        return self.mpan


class DataServiceMeter(models.Model):
    customer = models.ForeignKey(
        DataServiceCustomer, on_delete=models.DO_NOTHING, related_name="meters"
    )
    mpan = models.ForeignKey(
        DataServiceMPAN,
        on_delete=models.DO_NOTHING,
        related_name="meters",
        null=True,
        blank=True,
    )

    serial_number = models.CharField(max_length=64, null=True, blank=True)

    objects = DataServiceManager()

    class Meta:
        db_table = "meters"
        managed = False

    def __str__(self) -> str:
        return (
            f"MPAN: {getattr(self.mpan, 'mpan', '-')}, SN: {self.serial_number}"
        )


class DataServiceContractMeter(models.Model):
    contract = models.ForeignKey(
        DataServiceContract, on_delete=models.DO_NOTHING, related_name="meters"
    )
    meter = models.ForeignKey(
        DataServiceMeter, on_delete=models.DO_NOTHING, related_name="contracts"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    standing_charge = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    day_unit_rate = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    night_unit_rate = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    ewe_unit_rate = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    daily_capacity = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    capacity = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    total_eac = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    excess_capacity_charge = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    reactive_charge = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    distribution_charge = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    transmission_charge = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    climate_change_levy = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    mop_hh = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    da_dc_hh = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )
    night_start = models.TimeField(null=True, blank=True)
    night_end = models.TimeField(null=True, blank=True)

    objects = DataServiceManager()

    class Meta:
        db_table = "contract_meters"
        managed = False

    def __str__(self):
        return f"""
            Contract: {self.contract.name},
            Start-date: {self.start_date},
            End-date: {self.end_date}"
        """


class DataServiceMeterConsumption(models.Model):
    meter = models.ForeignKey(
        DataServiceMeter,
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
    created_at = models.DateTimeField()

    class Meta:
        db_table = "meter_consumptions"
        managed = False
