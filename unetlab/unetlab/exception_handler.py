import sys
import traceback as tb
from rest_framework.views import exception_handler
from http.client import responses
from django.conf import settings

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get("request", None)
    command = request.resolver_match.view_name
    payload = {
        "status": "error",
        "code": response.status_code,
        "message": response.status_text,
        "url": request.get_full_path(),
        "type": "response",
        "command": command,
        "data": response.data if response else None,
    }

    if settings.DEBUG:
        exc_type, exc_value, exc_tb = sys.exc_info()
        payload["traceback"] = "".join(tb.format_exception(exc_type, exc_value, exc_tb))

    response.data = payload if response else payload
    return response


