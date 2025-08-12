import django_tables2 as tables
from repository.models import Repository
from ui import messages
from ui.tables import GreenRedBooleanColumn, GreenRedReverseBooleanColumn


class RepositoryTable(tables.Table):
    name = tables.LinkColumn(
        "repository_detail",
        args=[tables.A("pk")],
    )
    uri = tables.TemplateColumn(
        orderable=False,
        template_code="{{ record.uri|truncatechars:60 }}",
    )
    is_enabled = GreenRedBooleanColumn(
        orderable=True, attrs={"td": {"class": "text-center"}}
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Repository
        exclude = ["select", "actions"]
        order_by = "name"
        attrs = {
            "title": messages.TABLE_REPOSITORY_TITLE,
            "description": messages.TABLE_REPOSITORY_DESCRIPTION,
            "detail_view": "repository_detail",
            "actions": [
                # {
                #     "action": "Add",
                #     "method": "POST",
                #     "view": "repository-add",
                # },
                # {
                #     "action": "Delete",
                #     "method": "POST",
                #     "view": "repository-add",
                # },
                # {
                #     "action": "Disable",
                #     "method": "POST",
                #     "view": "repository-disable",
                # },
                # {
                #     "action": "Enable",
                #     "method": "POST",
                #     "view": "repository-enable",
                # },
            ],
            "vip_actions": [
                {
                    "action": "Rescan",
                    "js": "rescan('repository')",
                },
            ],
        }


class RepositoryHomeTable(tables.Table):
    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Repository
        exclude = ["select", "actions"]
        order_by = "name"
        attrs = {
            "title": messages.TABLE_REPOSITORY_TITLE,
            "description": messages.TABLE_REPOSITORY_DESCRIPTION,
            # "detail_view": "host_detail",
        }
