import json
import secrets
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pymongo.errors import PyMongoError


def read_media_body(request):
    if request.content_type != "application/json":
        raise ValueError("application/json 본문을 보내세요.")
    data = json.loads(request.body)
    if not isinstance(data, dict):
        raise ValueError("JSON 객체가 필요합니다.")
    media_id = data.get("media_id")
    expected = settings.MEDIA_KEYS.get(media_id, "") if isinstance(media_id, str) else ""
    supplied = request.headers.get("X-Media-Key", "")
    if request.headers.get("X-Media-ID") != media_id or not expected or not secrets.compare_digest(
            expected.encode("utf-8"), supplied.encode("utf-8")):
        raise PermissionError("매체 인증 실패")
    subject = data.get("subject")
    if not isinstance(subject, dict) or subject.get("media_id") != media_id:
        raise ValueError("인증한 매체의 subject를 보내세요.")
    if not isinstance(subject.get("subject_id"), str) or not subject["subject_id"]:
        raise ValueError("공개 subject_id 문자열이 필요합니다.")
    return data, {"media_id": media_id, "subject_id": subject["subject_id"]}


def media_api_methods(*methods):
    def decorate(view):
        @csrf_exempt
        @require_http_methods(methods)
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            try:
                request.media_body, request.subject = read_media_body(request)
                return view(request, *args, **kwargs)
            except PermissionError:
                return JsonResponse({"error": "media_auth_required"}, status=401)
            except (ValueError, UnicodeDecodeError) as error:
                code = str(error).split(":", 1)[0]
                allowed = {"decision_snapshot_missing", "decision_not_found_for_subject",
                           "impression_required", "decision_id_required", "event_type_invalid"}
                return JsonResponse({"error": code if code in allowed else "invalid_event"}, status=400)
            except PyMongoError:
                return JsonResponse({"error": "ads_unavailable"}, status=503)
        return wrapped
    return decorate
