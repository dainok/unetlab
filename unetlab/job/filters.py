"""Django filters definitions for Job and Log models.

Provides filtering capabilities used in views and API endpoints
to enable users to filter Job and Log records by relevant fields.
"""

from django import forms
import django_filters
from job.models import Job, JobStatusChoices, Log, LogSeverityChoices
from ui.include.filters import SearchFilterSet


class JobFilter(SearchFilterSet):
    """FilterSet for filtering Job instances by username, status, and creation date.

    This filter is used primarily in list views and APIs to narrow down
    Job records based on selected criteria.

    Filters:
        - username: Dropdown choice of job owners dynamically populated
        - status: Job status, using JobStatusChoices enum
        - created_at__gte: Filter jobs created on or after a given date
        - created_at__lte: Filter jobs created on or before a given date
    """

    username = django_filters.ChoiceFilter(
        choices=[],  # Populated dynamically in __init__
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Owner",
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
        """
        Override initializer to dynamically set the user choices
        based on distinct users currently owning jobs.
        """
        super().__init__(*args, **kwargs)
        usernames = (
            Job.objects.order_by("username")
            .values_list("username", flat=True)
            .distinct()
        )
        self.filters["username"].extra["choices"] = [(u, u) for u in usernames]

    class Meta:
        model = Job
        fields = ["username", "status", "created_at__gte", "created_at__lte"]


class LogFilter(SearchFilterSet):
    """FilterSet for filtering Log instances by severity, acknowledgment, and creation date.

    This filter supports:
        - severity: Level of the log message, based on LogSeverityChoices
        - acknowledged: Boolean filter for whether the log was acknowledged
        - created_at__gte / created_at__lte: Date range filters for creation timestamp
    """

    search_fields = ["message"]
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
