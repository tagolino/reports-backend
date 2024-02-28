from django.contrib import admin

from .models import Customer, ElectricityCustomerAccount


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "customer_portal_id", "created_at"]
    empty_value_display = "-"
    search_fields = [
        "name",
    ]


@admin.register(ElectricityCustomerAccount)
class ElectricityCustomerAccountAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "customer_portal_eca_id", "created_at"]
    empty_value_display = "-"
    search_fields = [
        "name",
    ]
