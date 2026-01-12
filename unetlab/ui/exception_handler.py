"""Exception handler for UI app."""

import sys
import traceback
from http import HTTPStatus
from rest_framework.views import exception_handler
from django.conf import settings


def CustomExceptionHandler(exc, context):
    """Return exception in JSON format."""
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    response = exception_handler(exc, context)
    request = context.get('request', None)
    command = request.resolver_match.view_name
    payload = {
        'status': 'error',
        'http': {
            'code': status.value,
            'message': status.phrase,
            'url': request.get_full_path(),
        },
        'type': 'response',
        'command': command,
    }

    # Include traceback if DEBUG=True (you can control this as needed)
    if settings.DEBUG:
        exc_type, exc_value, exc_tb = sys.exc_info()
        payload['traceback'] = ''.join(
            traceback.format_exception(exc_type, exc_value, exc_tb)
        )

    return response
