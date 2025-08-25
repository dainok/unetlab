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
            "created_at",
            "updated_at",
        ]
        sequence = ["name", "..."]
        order_by = ["name"]


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
            "id",
            "nodes",
            "lld",
            # "created_at",
            "updated_at",
        ]
        sequence = ["lab", "..."]
        order_by = ["lab"]
        attrs = {
            "table_actions": [],
        }
