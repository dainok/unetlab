"""Filter definitions for Repository.

These filters are used in list views and API endpoints to provide
search functionality.
"""

from django import forms
import django_filters
from repository.models import Repository
from ui.include.filters import SearchFilterSet
from ui.include import messages


class RepositoryFilter(SearchFilterSet):
    """Filter class for the `Repository` model."""

    search_fields = ["name", "uri"]
    is_enabled = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=messages.CHOICES_YES_NO,
        ),
    )

    class Meta:
        model = Repository
        fields = ["is_enabled"]
