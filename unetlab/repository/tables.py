import django_tables2 as tables
from repository.models import Repository
from unetlab import messages


class RepositoryTable(tables.Table):
    uri = tables.TemplateColumn(
        orderable=False,
        template_code="{{ record.uri|truncatechars:60 }}",
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
                {
                    "action": "Add",
                    "method": "POST",
                    "view": "repository-add",
                },
                {
                    "action": "Delete",
                    "method": "POST",
                    "view": "repository-add",
                },
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
