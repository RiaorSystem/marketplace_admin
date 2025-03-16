from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """Custom Admin Panel for Managing Users"""
    
    list_display = ("email", "username", "role", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username", "role")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username", "role", "phone_number")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "role", "password1", "password2"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
