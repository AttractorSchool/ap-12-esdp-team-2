from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'email')
    list_display_links = ('phone',)
    fieldsets = (
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "avatar", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (None, {"fields": ("password",)}),
    )
    ordering = ("date_joined",)


admin.site.register(User, CustomUserAdmin)
