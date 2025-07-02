"""Views, called by URLs."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2025, Andrea Dainese"
__license__ = "GPLv3"

from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.conf import settings
from rest_framework import viewsets, mixins
from job.models import Log, Job
from job.serializers import JobSerializer


class JobQueryMixin:
    """Set common behaviour between UI and REST API."""

    def get_queryset(self):
        """Implement queryset filters."""
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Job.objects.all()
        return Job.objects.filter(user=user.username)

    def get_object(self):
        """Implement object filter."""
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or obj.user == user.username:
            return obj
        raise PermissionDenied()

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get("per_page")
        try:
            per_page = int(per_page)
            if per_page > 100:
                return 100
            return per_page
        except (TypeError, ValueError):
            return 10  # default


class JobViewSet(
    JobQueryMixin,
    mixins.ListModelMixin,  # GET /objects/
    mixins.RetrieveModelMixin,  # GET /objects/<id>/
    mixins.DestroyModelMixin,  # DELETE /jobs/<id>/
    viewsets.GenericViewSet,
):
    """Implement API class."""

    serializer_class = JobSerializer


class JobsListView(JobQueryMixin, ListView):
    """Implement list view class."""

    model = Job
    paginate_by = settings.REST_FRAMEWORK["PAGE_SIZE"]


class JobDetailView(JobQueryMixin, DetailView):
    """Implement detail view class."""

    model = Job
