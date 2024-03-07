from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)

    customer_portal_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "customers"

    def __str__(self) -> str:
        return self.name


class ElectricityCustomerAccount(models.Model):
    customer = models.ForeignKey(
        Customer,
        null=True,
        on_delete=models.SET_NULL,
        related_name="electricity_customer_accounts",
    )

    name = models.CharField(max_length=255)

    customer_portal_eca_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "electricity_customer_accounts"

    def __str__(self) -> str:
        return self.name
