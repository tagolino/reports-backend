from django.contrib import admin

from .models import (
    DataFileRequest,
    Document,
    DocumentDataFile,
    DocumentGenerationRequest,
)


class DocumentDataFileInline(admin.TabularInline):
    model = DocumentDataFile
    readonly_fields = ["name", "file"]

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DocumentGenerationRequestInline(admin.TabularInline):
    model = DocumentGenerationRequest
    readonly_fields = ["name", "status", "file", "error", "user"]
    exclude = ["json_data"]

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    empty_value_display = "-"
    search_fields = [
        "name",
    ]
    inlines = [DocumentDataFileInline, DocumentGenerationRequestInline]
    exclude = ["template_data_mapping"]

    def has_add_permission(self, request):
        return False


@admin.register(DataFileRequest)
class DataFileRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "period_start_at",
        "period_end_at",
        "created_by",
        "created_at",
    ]
