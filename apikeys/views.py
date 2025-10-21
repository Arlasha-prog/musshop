from django.http import JsonResponse
from .decorators import require_api_key

@require_api_key
def whoami(request):
    obj = request.api_key_obj
    return JsonResponse({
        'name': obj.name,
        'created': obj.created.isoformat(),
        'revoked': obj.revoked,
    })
