from django.contrib import admin
from .models import ApiKey

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "prefix", "is_active", "rate_limit", "created_at", "last_used_at")
    search_fields = ("name", "prefix")
    list_filter = ("is_active",)
