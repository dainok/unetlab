from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
import django_tables2 as tables
from ui import messages


class BooleanColumn(tables.TemplateColumn):
    """Rappresenta in una tabella un valore booleano con ☑️ (True) e ❌ (False).

    Esempio di utilizzo:

    ```
    class LogTable(tables.Table):
        acknowledged = GreenBooleanColumn()
    ````
    """

    def __init__(self, *args, **kwargs):
        """
        Inizializza l'oggetto applicando il template."""
        kwargs.setdefault("template_name", "unetlab/tables/column_boolean.html")
        super().__init__(*args, **kwargs)


class GreenBooleanColumn(tables.TemplateColumn):
    """Rappresenta in una tabella  un valore booleano con ✅ (True). False non viene rappresentato.

    Esempio di utilizzo:

    ```
    class LogTable(tables.Table):
        acknowledged = GreenBooleanColumn()
    ````
    """

    def __init__(self, *args, **kwargs):
        """
        Inizializza l'oggetto applicando il template."""
        kwargs.setdefault("template_name", "unetlab/tables/column_boolean_green.html")
        super().__init__(*args, **kwargs)


class GreenRedBooleanColumn(tables.TemplateColumn):
    """Rappresenta in una tabella  un valore booleano con ✅ (True) e ❌ (False).

    Esempio di utilizzo:

    ```
    class ProxmoxHostHomeTable(tables.Table):
        is_online = GreenRedBooleanColumn()
    ```
    """

    def __init__(self, *args, **kwargs):
        """
        Inizializza l'oggetto applicando il template."""

        kwargs.setdefault(
            "template_name", "unetlab/tables/column_boolean_green_red.html"
        )
        super().__init__(*args, **kwargs)


class GreenRedReverseBooleanColumn(tables.TemplateColumn):
    """Rappreenta in una tabella  un valore booleano con ❌ (True) e ✅ (False).

    Esempio di utilizzo:

    ```
    class ProxmoxHostHomeTable(tables.Table):
        is_orphan = GreenRedReverseBooleanColumn()
    ```
    """

    def __init__(self, *args, **kwargs):
        """
        Inizializza l'oggetto applicando il template."""
        kwargs.setdefault(
            "template_name", "unetlab/tables/column_boolean_green_red_reverse.html"
        )
        super().__init__(*args, **kwargs)


class SeverityColumn(tables.TemplateColumn):
    """Rappresenta in una tabella  i valori di severity error e warning (integer) in modo grafico.

    Esempio di utilizzo:

    ```
        class LogTable(ObjectTable):
        severity = SeverityColumn()
    ```
    """

    def __init__(self, *args, **kwargs):
        """
        Inizializza l'oggetto applicando il template."""
        kwargs.setdefault("template_name", "unetlab/tables/column_severity.html")
        super().__init__(*args, **kwargs)


class SeverityAllColumn(tables.TemplateColumn):
    """Rappresenta in una tabella  tutti i valori di severity in modo grafico.

    Esempio di utilizzo:

    ```
        class LogTable(ObjectTable):
        severity = SeverityAllColumn()
    ```
    """

    def __init__(self, *args, **kwargs):
        """
        Inizializza l'oggetto applicando il template."""
        kwargs.setdefault("template_name", "unetlab/tables/column_severity_all.html")
        super().__init__(*args, **kwargs)


class ObjectTable(tables.Table):
    """
    Tabella per un oggetto generico.

    La tabella inizializza a default i seguenti attributi:
    - title della tabella referenziando il valore in messages.TABLE_<model>_TITLE
    - description della tabella referenziando il valore in messages.TABLE_<model>_DESCRIPTION
    - detail_view con il valore <model>_detail

    I valori possono essere sovrascritti, anche singolarmente.

    La tabella viene renderizzata di default con i valori definiti in unetlab.settings:
    - DJANGO_TABLES2_PAGE_SIZE: la dimensione di default della pagina
    - DJANGO_TABLES2_MAX_PAGE_SIZE: la dimensione massima della pagina
    - DJANGO_TABLES2_TEMPLATE: il template di default

    Il template aggiunge automaticamente:
    - la colonna select, per selezionare manualmente più righe ed effettuare azioni
    - la colonna row_actions, per effettuare azioni su una singola riga (default: view, delete, edit)

    A livello di tabella sono inoltre presenti dei bottoni che permettono di effettuare azioni globalmente o su più righe. I bottono sono raggruppati in un meno a tendina (table_actions) o visibili direttamente (table_vip_actions).
    Ciascuna azione è definita nel seguente modo:

    ```
    {
        "button": "Delete", # Usata per descrivere il bottone
        "view": "group_list", # Usata se il bottone porta ad una vista specifica
        "js": "JsFunction", # Usata se il bottone richiama una specifica funzione JavaScript
    }
    ```

    Esempio di utilizzo:

    ```
    class GroupTable(ObjectTable):
        class Meta:
            model = Group
            template_name = "custom/table.html"
            attrs = {
                "title": "User groups"
            }
    ```
    """

    def __init__(self, *args, **kwargs):
        """
        Inizializza l'oggetto lasciando che tables.Table applichi Meta.attrs.

        I valori di title, description, detail_view e search vengono impostati se non presenti.
        """
        super().__init__(*args, **kwargs)
        model_name = self.Meta.model._meta.model_name.lower()

        # Imposta i valori di default se non presenti
        if "title" not in self.attrs:
            default_title = getattr(messages, f"TABLE_{model_name.upper()}_TITLE")
            self.attrs["title"] = default_title
        if "description" not in self.attrs:
            default_description = getattr(
                messages, f"TABLE_{model_name.upper()}_DESCRIPTION"
            )
            self.attrs["description"] = default_description
        if "detail_view" not in self.attrs:
            default_detail_view = f"{model_name}_detail"
            self.attrs["detail_view"] = default_detail_view
        if "search" not in self.attrs:
            self.attrs["search"] = True

        # Imposta le azioni di default se non presenti
        if "row_actions" not in self.attrs:
            row_actions = [
                {
                    "button": messages.VIEW,
                    "view": f"{model_name}_detail",
                }
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
                    "js": f"deleteSelected('{model_name}')",
                },
            ]
            self.attrs["table_actions"] = table_actions


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

    class Meta:
        """Imposta il modello per la tabella, definisce le colonne escluse, la sequenza delle colonne, l'ordinamenti di default."""

        model = Group
        exclude = ["id"]
        order_by = "group"


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
