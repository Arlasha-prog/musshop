from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([AllowAny])
def demo_api(request):
    if not request.auth:
        return Response({"detail": "API key required"}, status=401)
    return Response({"ok": True, "message": "Valid API key!"})
