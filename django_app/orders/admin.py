from django.contrib import admin 
from .models import Order 

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__email",)
    ordering = ("-created_at",)

admin.site.register(Order, OrderAdmin)
