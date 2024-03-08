from django_filters import rest_framework as filters

from .models import DataFileRequest, Document


class DocumentFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
        )
    )

    class Meta:
        model = Document
        fields = [
            "created_at",
        ]


class DataFileRequestFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
        )
    )

    class Meta:
        model = DataFileRequest
        fields = [
            "created_at",
        ]
