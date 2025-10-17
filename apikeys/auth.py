import hashlib, hmac
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import ApiKey

def hash_key(full_key: str):
    return hashlib.sha256(full_key.encode("utf-8")).hexdigest()

class ApiKeyAuthentication(BaseAuthentication):
    keyword = "X-API-Key"

    def authenticate(self, request):
        raw = request.headers.get(self.keyword) or request.query_params.get("api_key")
        if not raw:
            return None
        if "." not in raw:
            raise exceptions.AuthenticationFailed("Invalid API key format")

        prefix, secret = raw.split(".", 1)
        try:
            ak = ApiKey.objects.get(prefix=prefix, is_active=True)
        except ApiKey.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid or inactive API key")

        expected = ak.hashed_key
        actual = hash_key(raw)
        if not hmac.compare_digest(actual, expected):
            raise exceptions.AuthenticationFailed("Invalid API key")

        ak.last_used_at = timezone.now()
        ak.save(update_fields=["last_used_at"])
        request._request.auth = ak
        return (None, ak)
