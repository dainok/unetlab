import django_tables2 as tables
from node.models import NodeTemplate
from ui.tables import GreenRedBooleanColumn, GreenRedReverseBooleanColumn, URLColum
from unetlab import messages


class NodeTemplateTable(tables.Table):
    uri = URLColum(orderable=False)
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = NodeTemplate
        exclude = ["select", "actions"]
        order_by = "name"
        attrs = {
            "title": messages.TABLE_TEMPLATE_TITLE,
            "description": messages.TABLE_TEMPLATE_DESCRIPTION,
            "detail_view": "Template_detail",
            "actions": [
                {
                    "action": "Add",
                    "method": "POST",
                    "view": "Template-add",
                },
                {
                    "action": "Delete",
                    "method": "POST",
                    "view": "Template-add",
                },
            ],
            "vip_actions": [
                {
                    "action": "Rescan",
                    "js": "rescan('Template')",
                },
            ],
        }


class NodeTemplateHomeTable(tables.Table):
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = NodeTemplate
        exclude = ["select", "actions"]
        order_by = "name"
        attrs = {
            "title": messages.TABLE_TEMPLATE_TITLE,
            "description": messages.TABLE_TEMPLATE_DESCRIPTION,
            # "detail_view": "host_detail",
        }
