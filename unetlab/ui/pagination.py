from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    """Flexible pagination for REST API."""
    page_size = 10  # default
    page_size_query_param = "per_page"  # consente ?per_page=50
    max_page_size = 100  # limite massimo per_page
