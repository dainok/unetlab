"""Django filters definitions for ProxmoxHost models.

Provides filtering capabilities used in views and API endpoints
to enable users to filter ProxmoxHost records by relevant fields.
"""

from django import forms
import django_filters
from proxmox.models import ProxmoxHost
from ui.include.filters import SearchFilterSet


class ProxmoxHostFilter(SearchFilterSet):
    """FilterSet for filtering ProxmoxHost instances by username, status, and creation date.
    TODO

    This filter is used primarily in list views and APIs to narrow down
    Job records based on selected criteria.

    Filters:
        - username: Dropdown choice of job owners dynamically populated
        - status: Job status, using JobStatusChoices enum
        - created_at__gte: Filter jobs created on or after a given date
        - created_at__lte: Filter jobs created on or before a given date
    """

    is_online = django_filters.BooleanFilter(
        widget=forms.Select(
            attrs={"class": "form-select"},
            choices=[
                ("", "---------"),
                ("true", "Yes"),
                ("false", "No"),
            ],
        ),
        label="Online",
    )
    is_orphan = django_filters.BooleanFilter(
        widget=forms.Select(
            attrs={"class": "form-select"},
            choices=[
                ("", "---------"),
                ("true", "Yes"),
                ("false", "No"),
            ],
        ),
        label="Orphan",
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
        model = ProxmoxHost
        fields = ["is_online", "is_orphan", "created_at__gte", "created_at__lte"]
