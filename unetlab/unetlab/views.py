"""Views, called by URLs."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.views.generic import TemplateView

class HomeView(TemplateView):
    """Home page."""

    template_name = "unetlab/home.html"
