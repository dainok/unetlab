"""
Reusable table definitions using django-tables2.

This module provides generic and customizable table columns and table classes
for use in Django projects. It includes:
"""

import django_tables2 as tables
from ui.include import messages


class GroupColumn(tables.TemplateColumn):
    orderable=False
    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault("template_name", "ui/tables/column_group.html")
        super().__init__(*args, **kwargs)


class BooleanColumn(tables.TemplateColumn):
    """Represents a boolean value in a table with ☑️ (True) and ❌ (False).

    Example usage:

        class LogTable(tables.Table):
            acknowledged = BooleanColumn()
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault("template_name", "ui/tables/column_boolean.html")
        super().__init__(*args, **kwargs)


class GreenBooleanColumn(tables.TemplateColumn):
    """Represents a boolean value in a table with ✅ (True). False is not displayed.

    Example usage:

        class LogTable(tables.Table):
            acknowledged = GreenBooleanColumn()
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault("template_name", "ui/tables/column_boolean_green.html")
        super().__init__(*args, **kwargs)


class GreenRedBooleanColumn(tables.TemplateColumn):
    """Represents a boolean value in a table with ✅ (True) and ❌ (False).

    Example usage:

        class ProxmoxHostHomeTable(tables.Table):
            is_online = GreenRedBooleanColumn()
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""

        kwargs.setdefault("template_name", "ui/tables/column_boolean_green_red.html")
        super().__init__(*args, **kwargs)


class GreenRedReverseBooleanColumn(tables.TemplateColumn):
    """Represents a boolean value in a table with ❌ (True) and ✅ (False).

    Example usage:

        class ProxmoxHostHomeTable(tables.Table):
            is_orphan = GreenRedReverseBooleanColumn()
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault(
            "template_name", "ui/tables/column_boolean_green_red_reverse.html"
        )
        super().__init__(*args, **kwargs)


class SeverityColumn(tables.TemplateColumn):
    """Graphically represents severity values (integer) in a table.

    Example usage:

        class LogTable(tables.Table):
            severity = SeverityColumn()
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault("template_name", "ui/tables/column_severity.html")
        super().__init__(*args, **kwargs)


class SeverityAllColumn(tables.TemplateColumn):
    """Graphically represents all severity values in a table.

    Example usage:

        class LogTable(tables.Table):
            severity = SeverityAllColumn()
    """

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault("template_name", "ui/tables/column_severity_all.html")
        super().__init__(*args, **kwargs)


class ObjectTable(tables.Table):
    """Generic table for a model object with default attributes and actions.

    The table sets default values for:
        - title: fetched from messages.TABLE_<model>_TITLE
        - description: fetched from messages.TABLE_<model>_DESCRIPTION
        - detail_view: default view for object detail
        - search: enables search if not specified

    Default row and table actions are provided:
        - Row actions: view, edit, delete
        - Table actions: add, bulk delete

    Example usage:

        class GroupTable(ObjectTable):
            class Meta:
                model = Group
                template_name = "custom/table.html"
                attrs = {
                    "title": "User groups"
                }
    """

    def __init__(self, *args, **kwargs):
        """Initialize the table, setting defaults if not provided."""
        super().__init__(*args, **kwargs)
        model_name = self.Meta.model._meta.model_name.lower()

        # Set default title and description if not provided
        if "title" not in self.attrs:
            default_title = getattr(messages, f"TABLE_{model_name.upper()}_TITLE")
            self.attrs["title"] = default_title
        if "description" not in self.attrs:
            default_description = getattr(
                messages, f"TABLE_{model_name.upper()}_DESCRIPTION"
            )
            self.attrs["description"] = default_description
        if "search" not in self.attrs:
            self.attrs["search"] = True
        self.attrs["model"] = model_name

        # Set default row actions if not provided
        if "row_actions" not in self.attrs:
            row_actions = [
                {
                    "button": messages.VIEW,
                    "view": f"{model_name}_detail",
                },
                {
                    "button": messages.EDIT,
                    "view": f"{model_name}_update",
                },
                {
                    "button": messages.DELETE,
                    "view": f"{model_name}_delete",
                },
            ]
            self.attrs["row_actions"] = row_actions
        if "table_actions" not in self.attrs:
            table_actions = [
                {
                    "button": messages.ADD,
                    "view": f"{model_name}_create",
                },
                {
                    "button": messages.DELETE,
                    "js": f"ObjectBulkDeleteView('{model_name}')",
                },
            ]
            self.attrs["table_actions"] = table_actions
