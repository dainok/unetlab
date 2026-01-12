"""Reusable table and column definitions using django-tables2."""

from django.utils.translation import gettext_lazy as _
import django_tables2 as tables


class GreenDateInThePast(tables.TemplateColumn):
    """Represents a date in the past ✅ (True). False is not displayed."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault(
            'template_name', 'ui/tables/column_date_in_the_past_green.html'
        )
        super().__init__(*args, **kwargs)


class GreenRedDateInThePast(tables.TemplateColumn):
    """Represents a date in the past ✅ (True) and ❌ (False)."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault(
            'template_name', 'ui/tables/column_date_in_the_past_green_red.html'
        )
        super().__init__(*args, **kwargs)


class GreenDateInTheFuture(tables.TemplateColumn):
    """Represents a date in the future ✅ (True). False is not displayed."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault(
            'template_name', 'ui/tables/column_date_in_the_future_green.html'
        )
        super().__init__(*args, **kwargs)


class GreenRedDateInTheFuture(tables.TemplateColumn):
    """Represents a date in the future ✅ (True) and ❌ (False)."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault(
            'template_name', 'ui/tables/column_date_in_the_future_green_red.html'
        )
        super().__init__(*args, **kwargs)


class BooleanColumn(tables.TemplateColumn):
    """Represents a boolean value in a table with ☑️ (True) and ❌ (False)."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault('template_name', 'ui/tables/column_boolean.html')
        super().__init__(*args, **kwargs)


class GreenBooleanColumn(tables.TemplateColumn):
    """Represents a boolean value in a table with ✅ (True). False is not displayed."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault('template_name', 'ui/tables/column_boolean_green.html')
        super().__init__(*args, **kwargs)


class GreenRedBooleanColumn(tables.TemplateColumn):
    """Represents a boolean value in a table with ✅ (True) and ❌ (False)."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""

        kwargs.setdefault('template_name', 'ui/tables/column_boolean_green_red.html')
        super().__init__(*args, **kwargs)


class GreenRedReverseBooleanColumn(tables.TemplateColumn):
    """Represents a boolean value in a table with ❌ (True) and ✅ (False)."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault(
            'template_name', 'ui/tables/column_boolean_green_red_reverse.html'
        )
        super().__init__(*args, **kwargs)


class GroupColumn(tables.TemplateColumn):
    """Represents groups assigned to a user."""

    orderable = False

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault('template_name', 'ui/tables/column_group.html')
        super().__init__(*args, **kwargs)


class SeverityAllColumn(tables.TemplateColumn):
    """Graphically represents all severity values in a table."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault('template_name', 'ui/tables/column_severity_all.html')
        super().__init__(*args, **kwargs)


class SeverityColumn(tables.TemplateColumn):
    """Graphically represents severity values (integer) in a table."""

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault('template_name', 'ui/tables/column_severity.html')
        super().__init__(*args, **kwargs)


class UserColumn(tables.TemplateColumn):
    """Represents users assigned to a group."""

    orderable = False

    def __init__(self, *args, **kwargs):
        """Initialize the column and apply the default template."""
        kwargs.setdefault('template_name', 'ui/tables/column_user.html')
        super().__init__(*args, **kwargs)


class ObjectTable(tables.Table):
    """Generic table for a model object with default attributes and actions."""

    def __init__(self, *args, **kwargs):
        """Initialize the table, setting defaults if not provided."""
        super().__init__(*args, **kwargs)
        model_name = self.Meta.model._meta.model_name.lower()
        verbose_name_plural = self.Meta.model._meta.verbose_name_plural

        # Set default title and description if not provided
        if 'title' not in self.attrs:
            self.attrs['title'] = verbose_name_plural
        if 'description' not in self.attrs:
            self.attrs['description'] = ''

        # Enable free search
        if 'search' not in self.attrs:
            self.attrs['search'] = True

        self.attrs['model'] = model_name

        # Set default row actions if not provided
        if 'row_actions' not in self.attrs:
            row_actions = [
                {
                    'button': _('View'),
                    'view': f'{model_name}_detail',
                },
                {
                    'button': _('Edit'),
                    'view': f'{model_name}_update',
                },
                {
                    'button': _('Delete'),
                    'view': f'{model_name}_delete',
                },
            ]
            self.attrs['row_actions'] = row_actions

        # Set default table actions if not provided
        if 'table_actions' not in self.attrs:
            table_actions = [
                {
                    'button': _('Add'),
                    'view': f'{model_name}_create',
                },
                {
                    'button': _('Delete'),
                    'js': f"ObjectBulkDeleteView('{model_name}')",
                },
            ]
            self.attrs['table_actions'] = table_actions
