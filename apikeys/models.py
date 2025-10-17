from django.db import models

class ApiKey(models.Model):
    name = models.CharField(max_length=100, help_text="Имя клиента/ключа")
    prefix = models.CharField(max_length=12, unique=True, db_index=True)
    hashed_key = models.CharField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True)
    rate_limit = models.CharField(max_length=50, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.prefix}...)"
