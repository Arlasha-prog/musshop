from django.http import JsonResponse
from .models import APIKey

class APIKeyMiddleware:
    """Simple middleware that checks X-API-KEY header or api_key query param.
    Add 'apikeys.middleware.APIKeyMiddleware' to MIDDLEWARE (near the top) if you want it global.
    It sets request.api_key_obj when valid.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.META.get('HTTP_X_API_KEY')
        param = request.GET.get('api_key')
        key = header or param
        request.api_key_obj = None

        if key:
            try:
                obj = APIKey.objects.get(key=key, revoked=False)
                request.api_key_obj = obj
            except APIKey.DoesNotExist:
                return JsonResponse({'detail':'Invalid API key'}, status=401)

        return self.get_response(request)
