import django_tables2 as tables
from proxmox.models import ProxmoxHost
from ui.tables import GreenRedBooleanColumn, GreenRedReverseBooleanColumn
from unetlab import messages


class ProxmoxHostTable(tables.Table):
    is_online = GreenRedBooleanColumn(
        orderable=True, attrs={"td": {"class": "text-center"}}
    )
    is_orphan = GreenRedReverseBooleanColumn(
        orderable=True, attrs={"td": {"class": "text-center"}}
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = ProxmoxHost
        exclude = ["select", "actions"]
        order_by = "hostname"
        attrs = {
            "title": messages.TABLE_HOST_TITLE,
            "description": messages.TABLE_HOST_DESCRIPTION,
            "detail_view": "host_detail",
        }


class ProxmoxHostHomeTable(tables.Table):
    is_online = GreenRedBooleanColumn(
        orderable=True, attrs={"td": {"class": "text-center"}}
    )
    is_orphan = GreenRedReverseBooleanColumn(
        orderable=True, attrs={"td": {"class": "text-center"}}
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = ProxmoxHost
        exclude = ["select", "actions"]
        order_by = "hostname"
        attrs = {
            "title": messages.TABLE_HOST_TITLE,
            "description": messages.TABLE_HOST_DESCRIPTION,
            "detail_view": "host_detail",
        }
