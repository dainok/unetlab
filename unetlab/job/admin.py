"""Enable Django admin features for Proxmox hosts."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.contrib import admin
from .models import Job, Log


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """List jobs."""

    fields = [
        "id",
        "user",
        "status",
        "created_at",
        "updated_at",
    ]  # Fields display order in view/edit
    list_display = [
        "id",
        "user",
        "status",
        "created_at",
        "updated_at",
    ]  # Fields display order in table
    list_filter = [
        "user",
        "status",
    ]  # Fields included as filters
    readonly_fields = ["user", "status"]
    search_fields = []  # Fields included in the free search
    actions = ["delete_selected"]

    def has_add_permission(self, request):
        """Remove add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Remove change permission."""
        return False


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """List logs."""

    fields = [
        "type",
        "source",
        "severity",
        "message",
        "acknowledged",
        "created_at",
    ]  # Fields display order in view/edit
    list_display = [
        "id",
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
    ]  # Fields included as filters
    readonly_fields = ["message", "severity", "source", "type"]
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
