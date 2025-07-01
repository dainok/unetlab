"""Define Celery configuration."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2025, Andrea Dainese"
__license__ = "GPLv3"

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unetlab.settings")

app = Celery("unetlab")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
