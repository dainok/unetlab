import django_tables2 as tables
from lab.models import Lab, LabInstance
from ui.include.tables import (
    ObjectTable,
)


#############################################################################
# Lab
#############################################################################


class LabTable(ObjectTable):
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Lab
        exclude = [
            # "select",
            # "actions",
            "hld",
            "lld",
            "created_at",
            "updated_at",
        ]
        sequence = ["name", "..."]
        order_by = ["name"]
        attrs = {
            "row_actions": [
                {
                    "button": "Delete",
                    "view": "lab_delete",
                },
                {
                    "button": "Edit",
                    "view": "lab_update",
                },
                {
                    "button": "Start",
                    "js": "labinstance_detail",
                },
                {
                    "button": "View",
                    "view": "lab_detail",
                },
            ],
        }


#############################################################################
# Instance
#############################################################################


class LabInstanceTable(ObjectTable):
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = LabInstance
        exclude = [
            # "select",
            # "actions",
            # "id",
            # "nodes",
            # "hld",
            # "lld",
            # "created_at",
            # "updated_at",
        ]
        # sequence = ["lab", "..."]
        # order_by = ["lab"]
        # attrs = {
        #     "table_actions": [],
        # }
