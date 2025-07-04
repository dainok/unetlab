"""UNetLab URL Configuration for the job app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job.views import (
    JobViewSet,
    JobListView,
    JobDetailView,
    LogViewSet,
    LogListView,
    LogDetailView,
)

# DRF router for API endpoints of Job and Log viewsets
router = DefaultRouter()
router.register(r"job", JobViewSet, basename="job")
router.register(r"log", LogViewSet, basename="log")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    # List and detail views for Jobs (HTML views)
    path("job/", JobListView.as_view(), name="job_list"),
    path("job/<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    # List and detail views for Logs (HTML views)
    path("log/", LogListView.as_view(), name="log_list"),
    path("log/<int:pk>/", LogDetailView.as_view(), name="log_detail"),
    # Include API routes from DRF router
    path("api/", include(router.urls)),
]
