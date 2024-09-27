"""Views, called by URLs."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from unetlab import models


class HomeView(TemplateView):
    """Home page."""

    template_name = "unetlab/home.html"


class LabListView(ListView):
    """Summary view for Labs."""

    model = models.Lab


class LabDetailView(DetailView):
    """Detailed view for Lab."""

    model = models.Lab
