from functools import wraps
from django.http import JsonResponse

def require_api_key(view_func):
    """Decorator for views: requires that request.api_key_obj is set (middleware or manual check)."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if getattr(request, 'api_key_obj', None) is None:
            # try direct header check as fallback
            key = request.META.get('HTTP_X_API_KEY') or request.GET.get('api_key')
            if not key:
                return JsonResponse({'detail':'API key required'}, status=401)
            # lazy import to avoid circular import at top-level
            from .models import APIKey
            try:
                obj = APIKey.objects.get(key=key, revoked=False)
                request.api_key_obj = obj
            except APIKey.DoesNotExist:
                return JsonResponse({'detail':'Invalid API key'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped
