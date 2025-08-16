"""Custom pagination class for REST API using Django REST Framework."""

from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Flexible pagination for REST API.

    Attributes:
        page_size (int): Default number of items per page.
        page_size_query_param (str): Query parameter name to allow clients to
            override the default page size (e.g., ?per_page=50).
        max_page_size (int): Maximum allowed page size to prevent excessive
            results per request.
    """

    page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
    page_size_query_param = "per_page"
    max_page_size = settings.REST_FRAMEWORK["MAX_PAGE_SIZE"]
