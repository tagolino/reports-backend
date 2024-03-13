from django.db.models import Exists, OuterRef
from django_filters import BaseInFilter, NumberFilter
from django_filters import rest_framework as filters

from .models import (
    CustomerPortalAccountHolder,
    CustomerPortalAsset,
    CustomerPortalECA,
    CustomerPortalElectricityContract,
    CustomerPortalMeter,
    CustomerPortalMpan,
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


class CustomerPortalAssetFilters(filters.FilterSet):
    electricity_customer_account_ids = NumberInFilter(
        method="eca_filter", lookup_expr="in"
    )

    class Meta:
        model = CustomerPortalAsset
        fields = [
            "electricity_customer_account_ids",
        ]

    def eca_filter(self, queryset, name, value):
        subquery = CustomerPortalMeter.objects.filter(
            electricity_customer_account_id__in=value,
            asset_id=OuterRef("pk"),
        )

        return queryset.filter(Exists(subquery))


class CustomerPortalMpanFilters(filters.FilterSet):
    electricity_customer_account_ids = NumberInFilter(
        field_name="electricity_customer_account_id", lookup_expr="in"
    )

    class Meta:
        model = CustomerPortalMpan
        fields = [
            "electricity_customer_account_ids",
        ]
