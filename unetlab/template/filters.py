"""Django filters definitions for Template and Log models.

Provides filtering capabilities used in views and API endpoints
to enable users to filter Template and Log records by relevant fields.
"""

from django import forms
import django_filters
from template.models import NodeTemplate
from ui.filters import BaseSearchFilterSet


class NodeTemplateFilter(django_filters.FilterSet):
    """FilterSet for filtering Template instances by username, status, and creation date.

    This filter is used primarily in list views and APIs to narrow down
    Template records based on selected criteria.

    Filters:
        - username: Dropdown choice of Template owners dynamically populated
        - status: Template status, using TemplateStatusChoices enum
        - created_at__gte: Filter Templates created on or after a given date
        - created_at__lte: Filter Templates created on or before a given date
    """

    username = django_filters.ChoiceFilter(
        choices=[],  # Populated dynamically in __init__
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Owner",
    )
    created_at__gte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control mb-2"}),
        label="Created After",
    )
    created_at__lte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control mb-2"}),
        label="Created Before",
    )

    class Meta:
        model = NodeTemplate
        fields = ["name", "created_at__gte", "created_at__lte"]
