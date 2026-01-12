"""Table definitions for UI app."""

from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
import django_tables2 as tables
from ui.include.tables import (
    GreenRedBooleanColumn,
    GreenRedReverseBooleanColumn,
    ObjectTable,
)


#############################################################################
# Group
#############################################################################


class GroupTable(ObjectTable):
    """Table definition for the Group model."""

    name = tables.LinkColumn(
        'group_detail',
        args=[tables.A('pk')],
    )
    users = tables.Column(empty_values=(), orderable=False)

    class Meta:
        """Meta options."""

        exclude = ('id',)
        model = Group
        order_by = 'group'

    def render_users(self, record):
        """Render a comma-separated list of users in the group."""
        return ', '.join(user.username for user in record.user_set.all())


#############################################################################
# User
#############################################################################


class UserTable(ObjectTable):
    """Table definition for the User model."""

    date_joined = tables.DateColumn(orderable=True, format='Y-m-d')
    is_active = GreenRedBooleanColumn()
    is_staff = GreenRedReverseBooleanColumn(verbose_name=_('Staff'))
    is_superuser = GreenRedReverseBooleanColumn(verbose_name=_('Admin'))
    last_login = tables.DateColumn(orderable=True, format='Y-m-d H:i')
    username = tables.LinkColumn('user_detail', args=[tables.A('pk')])

    class Meta:
        """Meta options."""

        model = User
        exclude = ('id', 'password', 'date_joined', 'last_login')
        sequence = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_superuser',
            'is_staff',
        )
        order_by = 'username'


#############################################################################
# Token
#############################################################################


class TokenTable(ObjectTable):
    """Table definition for the Token model."""

    created = tables.DateColumn(orderable=True, format='Y-m-d')

    class Meta:
        """Meta options."""

        model = Token
        sequence = (
            'user',
            'key',
            'created',
        )
        attrs = {
            'search': False,
            'table_actions': [
                {
                    'button': _('Add'),
                    'js': 'TokenCreateView()',
                },
                {
                    'button': _('Delete'),
                    'js': "ObjectBulkDeleteView('token')",
                },
            ],
            'row_actions': [
                {
                    'button': _('Delete'),
                    'view': 'token_delete',
                },
            ],
        }
