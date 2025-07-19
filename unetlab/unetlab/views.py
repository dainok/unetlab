"""Views for UNetLab: entry points bound to URLs."""

from django.views.generic import TemplateView
from job.models import Log


class CommonMixin:
    """HTML list view for Logs with filtering and pagination."""

    def get_log_queryset(self):
        """Return un-ancknoledged logs, owned by the user."""
        user = self.request.user
        qs = Log.objects.filter(acknowledged=False, job__username=user.username).order_by(
            "-created_at"
        )[:10]
        return qs

    def get_context_data(self, **kwargs):
        """Add latest logs to context."""
        context = super().get_context_data(**kwargs)
        context["latest_logs"] = self.get_log_queryset()
        return context


class HomeView(CommonMixin, TemplateView):
    """
    Render the home page for authenticated users.

    The template is loaded from: templates/unetlab/home.html
    """

    template_name = "unetlab/home.html"
