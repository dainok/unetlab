"""UNetLab URL Configuration."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.contrib import admin
from django.urls import path, include

from unetlab import views

admin.site.login_template = "unetlab-admin/login.html"
admin.site.index_template = "unetlab-admin/index.html"
admin.autodiscover()

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    #     path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(r"accounts/", include("django.contrib.auth.urls")),
    path(r"admin/rq/", include("django_rq.urls")),
    path("admin/", admin.site.urls),
    path("lab/", views.LabListView.as_view()),
    path("lab/<pk>", views.LabDetailView.as_view()),
]
