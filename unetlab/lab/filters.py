"""Django filters definitions for ProxmoxHost models.

Provides filtering capabilities used in views and API endpoints
to enable users to filter ProxmoxHost records by relevant fields.
"""

from django import forms
import django_filters
from lab.models import Lab, LabInstance
from ui.include.filters import SearchFilterSet


#############################################################################
# Lab
#############################################################################


class LabFilter(SearchFilterSet):
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

    created_at__gte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created After",
    )
    created_at__lte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created Before",
    )

    class Meta:
        model = Lab
        fields = ["created_at__gte", "created_at__lte"]


#############################################################################
# Instance
#############################################################################


class LabInstanceFilter(SearchFilterSet):
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

    created_at__gte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created After",
    )
    created_at__lte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created Before",
    )

    class Meta:
        model = LabInstance
        fields = ["created_at__gte", "created_at__lte"]
