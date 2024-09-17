"""UNetLab URL Configuration"""

from django.contrib import admin
from django.urls import path

from unetlab import views

admin.site.login_template = "unetlab-admin/login.html"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("lab/", views.LabList.as_view()),
    path("lab/<pk>", views.LabDetail.as_view()),
]
