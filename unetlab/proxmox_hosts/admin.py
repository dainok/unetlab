"""Enable Django admin features for Proxmox hosts."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.contrib import admin
from .models import ProxmoxHost


@admin.register(ProxmoxHost)
class ProxmoxHostAdmin(admin.ModelAdmin):
    """List Proxmox hosts."""

    list_display = ["name", "is_online", "is_orphan"]  # Field display order
    list_filter = ["is_online", "is_orphan"]  # Fields included as filters
    readonly_fields = ["name", "is_online", "is_orphan"]
    search_fields = ["name"]  # Fields included in the free search
    actions = ["delete_selected", "rescan"]

    def has_add_permission(self, request):
        """Remove add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Remove change permission."""
        return False

    @admin.action(description="Rescan selected Proxmox hosts")
    def rescan(modeladmin, request, queryset):
        """Rescan Proxmox host."""
        # TODO
        pass
