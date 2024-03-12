from django.contrib import admin

from .models import (
    Supplier,
    Template,
    TemplateDataMapping,
    TemplateFile,
    TemplateSubType,
    TemplateType,
)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
    empty_value_display = "-"


class TemplateFileInline(admin.TabularInline):
    model = TemplateFile
    extra = 0
    exclude = ["external_id", "uploader", "language"]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type", "sub_type", "created_at"]
    list_filter = ["type"]
    empty_value_display = "-"
    search_fields = [
        "name",
    ]
    inlines = [TemplateFileInline]


class TemplateDataMappingInline(admin.TabularInline):
    model = TemplateDataMapping
    extra = 0


@admin.register(TemplateFile)
class TemplateFileAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "version", "created_at", "is_active"]
    list_filter = ["template"]
    empty_value_display = "-"
    search_fields = [
        "name",
    ]
    readonly_fields = ["external_id", "template", "file", "uploader"]
    inlines = [TemplateDataMappingInline]

    def has_add_permission(self, request):
        return False


@admin.register(TemplateType)
class TemplateTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(TemplateSubType)
class TemplateSubTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
