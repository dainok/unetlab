"""URL configuration for Task app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task.views import (
    TaskAPIViewSet,
    TaskListView,
    TaskDetailView,
    LogAPIViewSet,
    LogListView,
    LogDetailView,
)

# DRF router for API endpoints of Task and Log viewsets
router = DefaultRouter()
router.register(r'task', TaskAPIViewSet, basename='task')
router.register(r'log', LogAPIViewSet, basename='log')

# URL patterns for class-based views and API endpoints
urlpatterns = [
    #########################################################################
    # Task views (HTML)
    #########################################################################
    path('task/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
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
