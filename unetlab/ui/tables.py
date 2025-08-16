from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
import django_tables2 as tables
from ui.include import messages
from ui.include.tables import ObjectTable


class UserTable(ObjectTable):
    """Definisce la tabella User e il formato delle colonne.

    Questa tabella è utilizzata nella vista user_list.
    """

    username = tables.LinkColumn(
        "user_detail",
        args=[tables.A("pk")],
    )
    date_joined = tables.DateColumn(orderable=True, format="Y-m-d")
    last_login = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Imposta il modello per la tabella, definisce le colonne escluse, la sequenza delle colonne, l'ordinamenti di default."""

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


class GroupTable(ObjectTable):
    """Definisce la tabella Group e il formato delle colonne.

    Questa tabella è utilizzata nella vista group_list.
    """

    name = tables.LinkColumn(
        "group_detail",
        args=[tables.A("pk")],
    )
    users = tables.Column(empty_values=())

    class Meta:
        """Imposta il modello per la tabella, definisce le colonne escluse, la sequenza delle colonne, l'ordinamenti di default."""

        model = Group
        exclude = ["id"]
        order_by = "group"

    def render_users(self, record):
        # record è l'istanza di Group
        return ", ".join(user.username for user in record.user_set.all())


class TokenTable(tables.Table):
    """Definisce la tabella Group e il formato delle colonne.

    Questa tabella è utilizzata nella vista token_list.
    """

    created_at = tables.DateColumn(orderable=True, format="Y-m-d")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        """Imposta il modello per la tabella, definisce le colonne escluse, la sequenza delle colonne, l'ordinamenti di default."""

        model = Token
        exclude = ["select", "actions"]
        # order_by = "username"
        attrs = {
            "title": messages.TABLE_HOST_TITLE,
            "description": messages.TABLE_HOST_DESCRIPTION,
            "detail_view": "host_detail",
        }
