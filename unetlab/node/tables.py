import django_tables2 as tables
from node.models import NodeTemplate
from ui.include.tables import (
    ObjectTable,
)


class NodeTemplateTable(ObjectTable):
    created = tables.DateColumn(orderable=True, format='Y-m-d')
    updated = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    class Meta:
        model = NodeTemplate
        exclude = [
            'id',
            'name',
            'checksum',
            'mgmt',
            'disk_checksum',
            'nics',
            'username',
            'password',
            'created',
            'updated',
        ]
        sequence = ['vendor', 'os', 'version', 'extra', '...']
        order_by = ['vendor', 'os', 'version', 'extra']
        attrs = {
            'table_vip_actions': [
                {
                    'button': 'Rescan',
                    'js': "RescanView('repository')",
                },
            ],
            'row_actions': [
                {
                    'button': 'View',
                    'view': 'nodetemplate_detail',
                }
            ],
        }


class NodeTable(ObjectTable):
    class Meta:
        model = NodeTemplate
        exclude = []
        # sequence = ["vendor", "os", "version", "extra", "..."]
        # order_by = ["vendor", "os", "version", "extra"]
        # attrs = {
        #     "table_vip_actions": [
        #         {
        #             "button": "Rescan",
        #             "js": "RescanView('repository')",
        #         },
        #     ],
        #     "row_actions": [
        #         {
        #             "button": "View",
        #             "view": "nodetemplate_detail",
        #         }
        #     ],
        # }
