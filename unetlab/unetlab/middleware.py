"""Custom middlewares."""

from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve


class LoginRequiredMiddleware:
    """
    Middleware that blocks access to views unless the user is authenticated,
    except for publicly accessible URLs, the Django admin, and API endpoints.

    This middleware should be added after authentication middleware.
    """

    def __init__(self, get_response):
        """
        Initialize middleware and save the get_response callable.

        Args:
            get_response (callable): The next middleware or view in the chain.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the incoming request.

        If the path is part of the API or admin, it is allowed.
        If the user is not authenticated and the URL is not public,
        redirect to the logout redirect URL (usually login).

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Either the response or a redirect response.
        """
        # Allow API URLs (handled by DRF)
        if request.path.startswith("/api/"):
            return self.get_response(request)

        # Allow Django admin URLs
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        # For other URLs, check authentication
        if not request.user.is_authenticated:
            resolver_match = resolve(request.path)
            if resolver_match.view_name not in settings.PUBLIC_URLS:
                return redirect(settings.LOGOUT_REDIRECT_URL)

        # Proceed normally if authenticated or URL is public
        return self.get_response(request)
