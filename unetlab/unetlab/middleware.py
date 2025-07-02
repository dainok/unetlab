"""Middleware loaded by settings."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            # API are managed by REST framework
            return self.get_response(request)
        if not request.user.is_authenticated:
            resolver_match = resolve(request.path)
            if resolver_match.view_name not in settings.PUBLIC_URLS:
                return redirect(settings.LOGIN_REDIRECT_URL)
        return self.get_response(request)
