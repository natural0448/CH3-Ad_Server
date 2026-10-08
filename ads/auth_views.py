"""JSON authentication for advertiser accounts in the ads project."""
import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.debug import sensitive_variables
from django.views.decorators.http import require_GET, require_POST


@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})


@sensitive_variables("body", "password", "credentials")
def read_credentials(request):
    if request.content_type != "application/json":
        raise ValueError("invalid_json")
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("invalid_json")
    if not isinstance(body, dict):
        raise ValueError("invalid_json")
    username, password = body.get("username"), body.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        raise ValueError("missing_credentials")
    if not username.strip() or not password:
        raise ValueError("missing_credentials")
    return {"username": username.strip(), "password": password}


@require_POST
@sensitive_variables("credentials")
def login_view(request):
    try:
        credentials = read_credentials(request)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    user = authenticate(request, **credentials)
    if user is None:
        return JsonResponse({"authenticated": False}, status=401)
    login(request, user)
    return JsonResponse({"authenticated": True})


@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"authenticated": False})
