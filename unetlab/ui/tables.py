"""Table definitions for UI app."""

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
    """Table definition for the Group model."""

    name = tables.LinkColumn(
        "group_detail",
        args=[tables.A("pk")],
    )
    users = tables.Column(empty_values=())

    class Meta:
        """Meta options."""

        exclude = ("id",)
        model = Group
        order_by = "group"

    def render_users(self, record):
        """Render a comma-separated list of users in the group."""
        return ", ".join(user.username for user in record.user_set.all())


#############################################################################
# User
#############################################################################


class UserTable(ObjectTable):
    """Table definition for the User model."""

    date_joined = tables.DateColumn(orderable=True, format="Y-m-d")
    is_active = GreenRedBooleanColumn()
    is_staff = GreenRedReverseBooleanColumn(verbose_name="Staff")
    is_superuser = GreenRedReverseBooleanColumn(verbose_name="Admin")
    last_login = tables.DateColumn(orderable=True, format="Y-m-d H:i")
    username = tables.LinkColumn("user_detail", args=[tables.A("pk")])

    class Meta:
        """Meta options."""

        model = User
        exclude = ("id", "password", "date_joined", "last_login")
        sequence = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_superuser",
            "is_staff",
        )
        order_by = "username"


#############################################################################
# Token
#############################################################################


class TokenTable(ObjectTable):
    """Table definition for the Token model."""

    created = tables.DateColumn(orderable=True, format="Y-m-d")

    class Meta:
        """Meta options."""

        model = Token
        sequence = (
            "user",
            "key",
            "created",
        )
        attrs = {
            "search": False,
            "table_actions": [
                {
                    "button": messages.ADD,
                    "js": "TokenCreateView()",
                },
                {
                    "button": messages.DELETE,
                    "js": "ObjectBulkDeleteView('token')",
                },
            ],
            "row_actions": [
                {
                    "button": messages.DELETE,
                    "view": "token_delete",
                },
            ],
        }
