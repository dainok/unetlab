"""Views for UNetLab: entry points bound to URLs."""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Render the home page for authenticated users.

    The template is loaded from: templates/unetlab/home.html
    """

    template_name = "unetlab/home.html"
