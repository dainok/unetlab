"""App configuration for the job management app."""

from django.apps import AppConfig


class JobConfig(AppConfig):
    """
    Configuration class for the 'job' Django app.

    This class is used by Django to set application-specific attributes
    and execute startup logic like signal registration.
    """

    name = "job"  # Python path to the app
    verbose_name = "Jobs"  # Human-readable app name

    def ready(self):
        """
        Hook method for application startup.

        Import and register signals to ensure they are connected
        when the app is loaded by Django.
        """
        from job import signals  # noqa: F401 (import used for side effects only)
