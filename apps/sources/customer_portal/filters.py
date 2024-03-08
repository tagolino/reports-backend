from django_filters import BaseInFilter, NumberFilter
from django_filters import rest_framework as filters

from .models import (
    CustomerPortalAccountHolder,
    CustomerPortalECA,
    CustomerPortalElectricityContract,
)


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class CustomerPortalAccountHolderFilters(filters.FilterSet):
    customer_ids = NumberInFilter(field_name="customer_id", lookup_expr="in")

    class Meta:
        model = CustomerPortalAccountHolder
        fields = [
            "customer_ids",
        ]


class CustomerPortalECAFilters(filters.FilterSet):
    customer_ids = NumberInFilter(
        field_name="account_holder__customer_id", lookup_expr="in"
    )
    account_holder_ids = NumberInFilter(
        field_name="account_holder_id", lookup_expr="in"
    )

    class Meta:
        model = CustomerPortalECA
        fields = [
            "customer_ids",
            "account_holder_ids",
        ]


class CustomerPortalElectricityContractFilters(filters.FilterSet):
    electricity_customer_account_ids = NumberInFilter(
        field_name="account_id", lookup_expr="in"
    )

    class Meta:
        model = CustomerPortalElectricityContract
        fields = [
            "electricity_customer_account_ids",
        ]
