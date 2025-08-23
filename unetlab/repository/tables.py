import django_tables2 as tables
from repository.models import Repository
from ui.include.tables import (
    GreenRedBooleanColumn,
    ObjectTable,
)


class RepositoryTable(ObjectTable):
    is_enabled = GreenRedBooleanColumn(
        orderable=True, attrs={"td": {"class": "text-center"}}
    )
    name = tables.LinkColumn(
        "repository_detail",
        args=[tables.A("pk")],
    )
    uri = tables.TemplateColumn(
        orderable=False,
        template_code="{{ record.uri|truncatechars:60 }}",
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Repository
        exclude = ["updated_at"]
        order_by = "name"
        attrs = {
            "table_vip_actions": [
                {
                    "button": "Rescan",
                    "js": "RescanView('repository')",
                },
            ],
        }
