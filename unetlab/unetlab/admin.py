"""
Admin pages.

Enable Django admin features for UNetLab models.
"""

from django.contrib import admin
from unetlab import models

admin.site.register(models.Host)
admin.site.register(models.Lab)


#
# Repository
#


@admin.action(description="Rescan selected Repositories")
def repository_rescan(modeladmin, request, queryset):
    """Rescan Repository."""
    pass


@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    """List Repositories."""

    list_display = ["name", "uri"]
    readonly_fields = []
    actions = [repository_rescan]
