"""Views, called by URLs."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2025, Andrea Dainese"
__license__ = "GPLv3"

from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.db.models import Count, Prefetch
from rest_framework import viewsets, mixins
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from job.models import Log, Job
from job.serializers import JobSerializer, LogSerializer
from job.filters import JobFilter, LogFilter
from unetlab.utils import db_fields_to_dict


class JobQueryMixin:
    """Set common behaviour between UI and REST API."""

    def get_queryset(self):
        """Implement queryset filters."""
        qs = super().get_queryset()
        qs = qs.annotate(log_count=Count("logs"))
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(user=user.username)

    def get_object(self):
        """Implement object filter."""
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or obj.user == user.username:
            return obj
        raise PermissionDenied()

    def get_paginate_by(self, queryset):
        """Implement pagination."""
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
    mixins.ListModelMixin,  # GET /object/
    mixins.RetrieveModelMixin,  # GET /object/<id>/
    mixins.DestroyModelMixin,  # DELETE /object/<id>/
    viewsets.GenericViewSet,
):
    """Implement API class."""

    serializer_class = JobSerializer
    filterset_class = JobFilter
    filter_backends = [DjangoFilterBackend]


class JobListView(JobQueryMixin, FilterView, ListView):
    """Implement list view class."""

    model = Job
    filterset_class = JobFilter
    paginate_by = settings.REST_FRAMEWORK["PAGE_SIZE"]
    extra_context = {
        "job_fields": db_fields_to_dict(Job._meta.fields),
    }


class JobDetailView(JobQueryMixin, DetailView):
    """Implement detail view class."""

    model = Job

    def get_queryset(self):
        """Implement queryset filters."""
        return Job.objects.prefetch_related(
            Prefetch("logs", queryset=Log.objects.order_by("created_at"))
        )

    def get_context_data(self, **kwargs):
        """Provide additional content to the template."""
        context = super().get_context_data(**kwargs)
        context["job_fields"] = db_fields_to_dict(Job._meta.fields)
        context["log_fields"] = db_fields_to_dict(Log._meta.fields)
        context["log_list"] = self.object.logs.all()
        return context


class LogQueryMixin:
    """Set common behaviour between UI and REST API."""

    def get_queryset(self):
        """Implement queryset filters."""
        qs = super().get_queryset()
        qs = qs.select_related("job")
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(job__user=user.username)

    def get_object(self):
        """Implement object filter."""
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or obj.job.user == user.username:
            return obj
        raise PermissionDenied()

    def get_paginate_by(self, queryset):
        """Implement pagination."""
        per_page = self.request.GET.get("per_page")
        try:
            per_page = int(per_page)
            if per_page > 100:
                return 100
            return per_page
        except (TypeError, ValueError):
            return 10  # default


class LogViewSet(
    LogQueryMixin,
    mixins.ListModelMixin,  # GET /object/
    mixins.RetrieveModelMixin,  # GET /object/<id>/
    mixins.DestroyModelMixin,  # DELETE /object/<id>/
    viewsets.GenericViewSet,
):
    """Implement API class."""

    serializer_class = LogSerializer
    filterset_class = LogFilter
    filter_backends = [DjangoFilterBackend]


class LogListView(LogQueryMixin, FilterView, ListView):
    """Implement list view class."""

    model = Log
    filterset_class = LogFilter
    paginate_by = settings.REST_FRAMEWORK["PAGE_SIZE"]
    extra_context = {
        "log_fields": db_fields_to_dict(Log._meta.fields),
        "job_fields": db_fields_to_dict(Job._meta.fields),
    }


class LogDetailView(LogQueryMixin, DetailView):
    """Implement detail view class."""

    model = Log

    def get_context_data(self, **kwargs):
        """Provide additional content to the template."""
        context = super().get_context_data(**kwargs)
        context["job_fields"] = db_fields_to_dict(Job._meta.fields)
        context["log_fields"] = db_fields_to_dict(Log._meta.fields)
        return context
