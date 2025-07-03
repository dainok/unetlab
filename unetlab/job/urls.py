"""UNetLab URL Configuration."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

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

router = DefaultRouter()
router.register(r"job", JobViewSet, basename="job")
# router.register(r'logs', LogViewSet, basename='log')

urlpatterns = [
    path("job/", JobListView.as_view(), name="job_list"),
    path("job/<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path("log/", LogListView.as_view(), name="log_list"),
    path("log/<int:pk>/", LogDetailView.as_view(), name="log_detail"),
    path("api/", include(router.urls)),
]

# urlpatterns = [
#     path("", views.HomeView.as_view(), name="home"),
#     #     path("", TemplateView.as_view(template_name="home.html"), name="home"),
#     path(r"accounts/", include("django.contrib.auth.urls")),
#     path(r"admin/rq/", include("django_rq.urls")),
#     path("admin/", admin.site.urls),
#     path("lab/", views.LabListView.as_view()),
#     path("lab/<pk>", views.LabDetailView.as_view()),
# ]
