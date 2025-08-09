import django_tables2 as tables
from node.models import NodeTemplate
from unetlab import messages


class NodeTemplateTable(tables.Table):
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = NodeTemplate
        exclude = [
            "select",
            # "actions",
            "id",
            "name",
            "checksum",
            "mgmt",
            "disks",
            "username",
            "password",
            "created_at",
            "updated_at",
        ]
        sequence = ["vendor", "os", "version", "extra", "..."]
        order_by = ["vendor", "os", "version", "extra"]
        attrs = {
            "title": messages.TABLE_TEMPLATE_TITLE,
            "description": messages.TABLE_TEMPLATE_DESCRIPTION,
            "detail_view": "template_detail",
            "actions": [
                {
                    "action": "Add",
                    "view": "template_create",
                },
                # {
                #     "action": "Delete",
                #     "method": "POST",
                #     "view": "template-delete",
                # },
            ],
        }


class NodeTemplateHomeTable(tables.Table):
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = NodeTemplate
        exclude = ["select", "actions", "name"]
        order_by = ["vendor", "os", "version", "extra"]
        attrs = {
            "title": messages.TABLE_TEMPLATE_TITLE,
            "description": messages.TABLE_TEMPLATE_DESCRIPTION,
            # "detail_view": "host_detail",
        }
