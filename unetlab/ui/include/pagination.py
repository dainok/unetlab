"""Custom pagination class for REST API using Django REST Framework."""

from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Flexible pagination for REST API."""

    page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
    page_size_query_param = "per_page"
    max_page_size = settings.REST_FRAMEWORK["MAX_PAGE_SIZE"]
