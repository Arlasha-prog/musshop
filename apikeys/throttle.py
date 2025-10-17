from rest_framework.throttling import SimpleRateThrottle

class ApiKeyRateThrottle(SimpleRateThrottle):
    scope = "apikey"

    def get_cache_key(self, request, view):
        api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
        if not api_key:
            return None
        prefix = api_key.split(".", 1)[0] if "." in api_key else "invalid"
        return f"throttle_{self.scope}_{prefix}"

    def get_rate(self):
        request = getattr(self, "request", None)
        if request and getattr(request, "auth", None) and getattr(request.auth, "rate_limit", ""):
            return request.auth.rate_limit
        return super().get_rate()
