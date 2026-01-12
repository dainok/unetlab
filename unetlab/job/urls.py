"""UNetLab URL Configuration for the job app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job.views import (
    JobAPIViewSet,
    JobListView,
    JobDetailView,
    LogAPIViewSet,
    LogListView,
    LogDetailView,
)

# DRF router for API endpoints of Job and Log viewsets
router = DefaultRouter()
router.register(r'job', JobAPIViewSet, basename='job')
router.register(r'log', LogAPIViewSet, basename='log')

# URL patterns for class-based views and API endpoints
urlpatterns = [
    #########################################################################
    # Job views (HTML)
    #########################################################################
    path('job/', JobListView.as_view(), name='job_list'),
    path('job/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    #########################################################################
    # Log views (HTML)
    #########################################################################
    path('log/', LogListView.as_view(), name='log_list'),
    path('log/<int:pk>/', LogDetailView.as_view(), name='log_detail'),
    #########################################################################
    # API endpoints
    #########################################################################
    path('api/', include(router.urls)),
]
