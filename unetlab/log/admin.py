"""Enable Django admin features for Proxmox hosts."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.contrib import admin
from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """List logs."""

    fields = [
        "user",
        "type",
        "source",
        "severity",
        "message",
        "acknowledged",
        "created_at",
    ]  # Fields display order in view/edit
    list_display = [
        "user",
        "type",
        "source",
        "severity",
        "message",
        "acknowledged",
        "created_at",
    ]  # Fields display order in table
    list_filter = [
        "acknowledged",
        "severity",
        "source",
        "type",
        "user",
    ]  # Fields included as filters
    readonly_fields = ["message", "severity", "source", "type", "user"]
    search_fields = [
        "message",
    ]  # Fields included in the free search
    actions = ["acknowledge", "delete_selected"]

    def has_add_permission(self, request):
        """Remove add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Remove change permission."""
        return False

    @admin.action(description="Acknowledge logs")
    def acknowledge(modeladmin, request, queryset):
        """Acknowledge logs."""
        # TODO
        pass
