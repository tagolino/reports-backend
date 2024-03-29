from django_filters import BaseInFilter, BooleanFilter, NumberFilter
from django_filters import rest_framework as filters

from .models import DataFileRequest, Document


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class DocumentFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("created_at", "created_at"),
            ("created_by", "created_by"),
            ("is_customer", "is_customer"),
            ("is_production", "is_production"),
            ("documents_count", "documents_count"),
        )
    )
    template_id = NumberInFilter(
        field_name="template_data_mapping__template_file__template",
        lookup_expr="in",
    )
    is_customer = BooleanFilter(field_name="is_customer")
    is_production = BooleanFilter(field_name="is_production")

    class Meta:
        model = Document
        fields = [
            "created_at",
        ]


class DataFileRequestFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(fields=(("created_at", "created_at"),))

    class Meta:
        model = DataFileRequest
        fields = [
            "created_at",
        ]
