"""Define Django filters used in View."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

import django_filters
from job.models import Job

class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            "status": ["exact"],
            "user": ["exact"],
            "created_at": ["date__gte", "date__lte"],
        }
