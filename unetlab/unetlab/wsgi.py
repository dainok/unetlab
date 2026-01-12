"""WSGI config for unetlab project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unetlab.settings')

application = get_wsgi_application()
