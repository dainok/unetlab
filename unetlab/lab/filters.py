"""Filter definitions for Lab app."""

from django import forms
import django_filters
from django.utils.translation import gettext_lazy as _
from lab.models import Lab
from ui.include.filters import SearchFilterSet


#############################################################################
# Lab
#############################################################################


class LabFilter(SearchFilterSet):
    """Filter class for the Lab model."""

    search_fields = ["name"]
    created_at__gte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Created after"),
    )
    created_at__lte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Created before"),
    )
    updated_at__gte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Updated after"),
    )
    updated_at__lte = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Updated before"),
    )

    class Meta:
        model = Lab
        fields = [
            "created_at__gte",
            "created_at__lte",
            "updated_at__gte",
            "updated_at__lte",
        ]


#############################################################################
# Instance
#############################################################################


# class LabInstanceFilter(SearchFilterSet):
#     """FilterSet for filtering ProxmoxHost instances by username, status, and creation date.
#     TODO

#     This filter is used primarily in list views and APIs to narrow down
#     Job records based on selected criteria.

#     Filters:
#         - username: Dropdown choice of job owners dynamically populated
#         - status: Job status, using JobStatusChoices enum
#         - created_at__gte: Filter jobs created on or after a given date
#         - created_at__lte: Filter jobs created on or before a given date
#     """
#     created_at__gte = django_filters.DateFilter(
#         field_name="created_at",
#         lookup_expr="gte",
#         widget=forms.DateInput(attrs={"type": "date"}),
#         label="Created After",
#     )
#     created_at__lte = django_filters.DateFilter(
#         field_name="created_at",
#         lookup_expr="lte",
#         widget=forms.DateInput(attrs={"type": "date"}),
#         label="Created Before",
#     )

#     class Meta:
#         model = LabInstance
#         fields = ["created_at__gte", "created_at__lte"]
