"""Views, called by URLs."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2025, Andrea Dainese"
__license__ = "GPLv3"

from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, mixins
from job.models import Log, Job
from job.serializers import JobSerializer


class JobQueryMixin:
    """Filter objects."""

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


class JobDetailView(JobQueryMixin, DetailView):
    """Implement detail view class."""

    model = Job
