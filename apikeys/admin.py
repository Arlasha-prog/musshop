from django.contrib import admin
from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'key', 'created', 'revoked')
    readonly_fields = ('key','created')
    search_fields = ('name','key')
    list_filter = ('revoked','created')
