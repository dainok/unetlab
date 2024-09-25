"""UNetLab URL Configuration"""

from django.contrib import admin
from django.urls import path

from unetlab import views

admin.site.login_template = "unetlab-admin/login.html"

urlpatterns = [
    path("", views.HomeView.as_view()),
    path("admin/", admin.site.urls),
    path("lab/", views.LabListView.as_view()),
    path("lab/<pk>", views.LabDetailView.as_view()),
]
