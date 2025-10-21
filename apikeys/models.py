import secrets
from django.db import models

def generate_key():
    # 40 chars hex ~ 160 bits
    return secrets.token_hex(20)

class APIKey(models.Model):
    name = models.CharField(max_length=150, blank=True, help_text='Human-friendly name / purpose')
    key = models.CharField(max_length=80, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_key()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name or self.key[:8]}{' (revoked)' if self.revoked else ''}"
