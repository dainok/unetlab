"""Enable Django admin features for Proxmox hosts."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.urls import path
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin
from proxmox.models import ProxmoxHost
from proxmox.tasks import do_rescan


@admin.register(ProxmoxHost)
class ProxmoxHostAdmin(admin.ModelAdmin):
    """List Proxmox hosts."""

    fields = [
        "name",
        "ip_address",
        "is_online",
        "is_orphan",
    ]  # Fields display order in view/edit
    list_display = [
        "name",
        "ip_address",
        "is_online",
        "is_orphan",
        "updated_at",
    ]  # Fields display order in table
    list_filter = ["is_online", "is_orphan"]  # Fields included as filters
    readonly_fields = ["name", "is_online", "is_orphan"]
    search_fields = ["name"]  # Fields included in the free search
    actions = ["delete_selected", "provision_selected"]

    # Custom action URLs
    _rescan_url = "rescan"
    _provision_url = "provision"

    def has_add_permission(self, request):
        """Remove add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Remove change permission."""
        return False

    def get_urls(self):
        """Override get_urls and add custom actions."""
        urls = super().get_urls()
        custom_urls = [
            path(
                self._rescan_url,
                self.admin_site.admin_view(self.rescan_view),
                name="proxmox_proxmoxhost_rescan",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """Override changelist_view and add custom actions."""
        if extra_context is None:
            extra_context = {}
        extra_context["rescan_url"] = self._rescan_url
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description="Provision selected Proxmox hosts")
    def provision_selected(self, request, queryset):
        """Provision selected Proxmox hosts."""
        pass
        # # TODO: should override PUT method
        # if not queryset.exists():
        #     queryset = self.get_queryset(request)

        # count = 0
        # for node in queryset:
        #     try:
        #         self._provision_node(node)
        #         count += 1
        #     except Exception as e:
        #         messages.error(request, f"Errore nel provisioning di {node}: {e}")

        # messages.success(request, f"Provisioning completato su {count} nodi.")

    def rescan_view(self, request):
        """Start rescan and return to changelist page."""
        do_rescan(user=request.user.username)
        return HttpResponseRedirect(reverse("admin:proxmox_proxmoxhost_changelist"))
