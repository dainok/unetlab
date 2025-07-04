"""Define Django filters used in View."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django import forms
import django_filters
from job.models import Job, JobStatusChoices, Log, LogSeverityChoices


class JobFilter(django_filters.FilterSet):
    """Filter for Job model used in list views and APIs."""

    user = django_filters.ChoiceFilter(
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"}),
        label="User",
    )
    status = django_filters.ChoiceFilter(
        choices=JobStatusChoices.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Status",
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

    def __init__(self, *args, **kwargs):
        """Dynamically populate user choices from existing Jobs."""
        super().__init__(*args, **kwargs)
        users = Job.objects.order_by("user").values_list("user", flat=True).distinct()
        self.filters["user"].extra["choices"] = [(u, u) for u in users]

    class Meta:
        model = Job
        fields = ["user", "status", "created_at__gte", "created_at__lte"]


class LogFilter(django_filters.FilterSet):
    """Filter for Log model used in list views and APIs."""

    acknowledged = django_filters.BooleanFilter(
        widget=forms.Select(
            attrs={"class": "form-select"},
            choices=[
                ("", "---------"),
                ("true", "Yes"),
                ("false", "No"),
            ],
        ),
        label="Acknowledged",
    )
    severity = django_filters.ChoiceFilter(
        choices=LogSeverityChoices.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Severity",
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
        model = Log
        fields = ["severity", "acknowledged", "created_at__gte", "created_at__lte"]
