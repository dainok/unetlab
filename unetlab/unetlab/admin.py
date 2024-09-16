"""
Admin pages.

Enable Django admin features for UNetLab models.
"""

from django.contrib import admin
from unetlab import models

admin.site.register(models.Host)
admin.site.register(models.Lab)
admin.site.register(models.Repository)
