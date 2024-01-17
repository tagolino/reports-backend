from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    """
    Users administration page class
    """

    model = User
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "is_active",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_staff", "is_superuser"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = [
        "id",
        "get_name",
        "email",
        "is_active",
        "created_at",
    ]
    list_filter = [
        "is_active",
    ]
    empty_value_display = "-"
    search_fields = ["first_name", "last_name", "email"]
    exclude = [
        "last_login",
        "groups",
        "user_permissions",
        "date_joined",
        "username",
    ]
    ordering = ["-id"]

    @admin.display(description="name")
    def get_name(self, instance: User):
        return instance.get_full_name()
