"""Celery application instance for UNetLab.

This file sets up the Celery app, allowing Django tasks to be executed
asynchronously. It loads configuration from Django settings using the
CELERY_ prefix and autodiscovers tasks in all registered apps.
"""

import os
from celery import Celery

# Set default Django settings module for the 'celery' CLI.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unetlab.settings')

# Create the Celery application instance.
app = Celery('unetlab')

# Load Celery settings from Django's settings.py using the "CELERY_" namespace.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py in all installed apps.
app.autodiscover_tasks()


# Optional debug task for testing Celery installation
@app.task(bind=True)
def debug_task(self):
    """Task used to debug Celery setup."""
    print(f'[Celery] Debug Task - Request: {self.request!r}')
