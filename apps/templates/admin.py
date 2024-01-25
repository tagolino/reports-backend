from django.contrib import admin

from .models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """
    Templates administration page class
    """

    model = Template
    list_display = ["id", "name", "type", "created_at"]
    list_filter = ["type"]
    empty_value_display = "-"
    search_fields = [
        "name",
    ]
