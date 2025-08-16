"""Generic reusable search filter for Django models.

This filter extends `django_filters.FilterSet` and allows subclasses
to define a list of searchable fields via `search_fields`.
"""

from django.db.models import Q
import django_filters


class SearchFilterSet(django_filters.FilterSet):
    """Base filter class providing a generic text search.

    Subclasses must define `search_fields` as a list of model fields
    that should be included in the search.
    """

    search = django_filters.CharFilter(method="filter_search")
    search_fields = []

    def filter_search(self, queryset, name, value):
        """Apply a case-insensitive `icontains` filter across all search fields.

        Args:
            queryset (QuerySet): The initial queryset to filter.
            name (str): The name of the filter field (unused).
            value (str): The search term entered by the user.

        Returns:
            QuerySet: The filtered queryset.
        """
        if not self.search_fields:
            return queryset
        q_objects = Q()
        for field in self.search_fields:
            q_objects |= Q(**{f"{field}__icontains": value})
        return queryset.filter(q_objects)
