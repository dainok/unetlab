import django_tables2 as tables
from django.conf import settings
from proxmox.models import ProxmoxHost
from unetlab.tables import GreenRedBooleanColumn, GreenRedReverseBooleanColumn

class ProxmoxHostTable(tables.Table):
    is_online = GreenRedBooleanColumn(orderable=True, attrs={"td": {"class": "text-center"}})
    is_orphan = GreenRedReverseBooleanColumn(orderable=True, attrs={"td": {"class": "text-center"}})
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = ProxmoxHost
        exclude = ["select", "actions"]