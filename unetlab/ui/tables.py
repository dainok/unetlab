"""Table definitions for User, Group, and Token models.

These tables are used in the corresponding list views to render
HTML tables with django-tables2.
"""

from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
import django_tables2 as tables
from ui.include import messages
from ui.include.tables import (
    GreenRedBooleanColumn,
    GreenRedReverseBooleanColumn,
    ObjectTable,
)


#############################################################################
# Group
#############################################################################


class GroupTable(ObjectTable):
    """Table definition for the `Group` model.

    Used in the `group_list` view.
    """

    name = tables.LinkColumn(
        "group_detail",
        args=[tables.A("pk")],
    )
    users = tables.Column(empty_values=())

    class Meta:
        """Meta options for the `GroupTable`.

        - Defines the underlying model.
        - Excludes unused fields.
        - Sets default ordering.
        """

        model = Group
        exclude = ["id"]
        order_by = "group"

    def render_users(self, record):
        """Render a comma-separated list of users in the group."""
        return ", ".join(user.username for user in record.user_set.all())


#############################################################################
# Token
#############################################################################


class TokenTable(tables.Table):
    """Table definition for the `Token` model.

    Used in the `token_list` view.
    """

    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options for the `TokenTable`.

        - Defines the underlying model.
        - Excludes unused fields.
        - Sets additional table attributes.
        """

        model = Token
        exclude = ["select", "actions"]
        # order_by = "username"
        attrs = {
            "title": messages.TABLE_HOST_TITLE,
            "description": messages.TABLE_HOST_DESCRIPTION,
            "detail_view": "host_detail",
        }


#############################################################################
# User
#############################################################################


class UserTable(ObjectTable):
    """Table definition for the `User` model.

    Used in the `user_list` view.
    """

    is_active = GreenRedBooleanColumn()
    is_staff = GreenRedReverseBooleanColumn()
    is_superuser = GreenRedReverseBooleanColumn()
    username = tables.LinkColumn(
        "user_detail",
        args=[tables.A("pk")],
    )
    date_joined = tables.DateColumn(orderable=True, format="Y-m-d")
    last_login = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Meta options for the `UserTable`.

        - Defines the underlying model.
        - Excludes sensitive or unused fields.
        - Sets column sequence and default ordering.
        """

        model = User
        exclude = ["select", "actions", "id", "password", "date_joined"]
        sequence = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_superuser",
            "is_staff",
            "...",
        ]
        order_by = "username"
