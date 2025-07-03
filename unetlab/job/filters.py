"""Define Django filters used in View."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django import forms
import django_filters
from job.models import Job, JobStatusChoices


class JobFilter(django_filters.FilterSet):
    user = django_filters.ChoiceFilter(
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = django_filters.ChoiceFilter(
        choices=JobStatusChoices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    created_at = django_filters.DateFilter(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control mb-2"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = Job.objects.order_by("user").values_list("user", flat=True).distinct()
        self.filters["user"].extra["choices"] = [(u, u) for u in users]

    class Meta:
        model = Job
        fields = {
            "status": ["exact"],
            "user": ["exact"],
            "created_at": ["date__gte", "date__lte"],
        }
