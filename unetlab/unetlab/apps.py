from django.apps import AppConfig

class UNetLabConfig(AppConfig):
    name = "unetlab"
    verbose_name = "UNetLab"

    def ready(self):
        """Registering signals."""
        from . import signals
