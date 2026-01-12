import django_tables2 as tables
from proxmox.models import ProxmoxHost
from ui.include.tables import (
    GreenRedBooleanColumn,
    GreenRedReverseBooleanColumn,
    ObjectTable,
)


class ProxmoxHostTable(ObjectTable):
    name = tables.LinkColumn(
        'host_detail',
        args=[tables.A('name')],
    )
    is_online = GreenRedBooleanColumn(
        orderable=True, attrs={'td': {'class': 'text-center'}}
    )
    is_orphan = GreenRedReverseBooleanColumn(
        orderable=True, attrs={'td': {'class': 'text-center'}}
    )
    created_at = tables.DateColumn(orderable=True, format='Y-m-d')
    updated_at = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    class Meta:
        model = ProxmoxHost
        exclude = ['select', 'actions']
        order_by = 'name'
        attrs = {
            'table_actions': [],
            'table_vip_actions': [
                {
                    'button': 'Rescan',
                    'js': "RescanView('host')",
                },
            ],
        }


class ProxmoxHostHomeTable(tables.Table):
    is_online = GreenRedBooleanColumn(
        orderable=True, attrs={'td': {'class': 'text-center'}}
    )
    is_orphan = GreenRedReverseBooleanColumn(
        orderable=True, attrs={'td': {'class': 'text-center'}}
    )
    created_at = tables.DateColumn(orderable=True, format='Y-m-d')
    updated_at = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    class Meta:
        model = ProxmoxHost
        exclude = ['select', 'actions']
        order_by = 'hostname'
