"""Django filters definitions for Template and Log models.

Provides filtering capabilities used in views and API endpoints
to enable users to filter Template and Log records by relevant fields.
"""

import django_filters
from node.models import Node, NodeTemplate
from ui.include.filters import SearchFilterSet


class NodeFilter(SearchFilterSet):
    """FilterSet for filtering Template instances by username, status, and creation date.

    This filter is used primarily in list views and APIs to narrow down
    Template records based on selected criteria.

    Filters:
        - username: Dropdown choice of Template owners dynamically populated
        - status: Template status, using TemplateStatusChoices enum
        - created_at__gte: Filter Templates created on or after a given date
        - created_at__lte: Filter Templates created on or before a given date
    """

    class Meta:
        model = Node
        fields = ["running_name"]


class NodeTemplateFilter(SearchFilterSet):
    """FilterSet for filtering Template instances by username, status, and creation date.

    This filter is used primarily in list views and APIs to narrow down
    Template records based on selected criteria.

    Filters:
        - username: Dropdown choice of Template owners dynamically populated
        - status: Template status, using TemplateStatusChoices enum
        - created_at__gte: Filter Templates created on or after a given date
        - created_at__lte: Filter Templates created on or before a given date
    """

    search_fields = ["name", "checksum"]
    extra = django_filters.ChoiceFilter(
        choices=[],  # Populated dynamically in __init__
        label="Extra",
    )
    os = django_filters.ChoiceFilter(
        choices=[],  # Populated dynamically in __init__
        label="OS",
    )
    username = django_filters.ChoiceFilter(
        choices=[],  # Populated dynamically in __init__
        label="Username",
    )
    vendor = django_filters.ChoiceFilter(
        choices=[],  # Populated dynamically in __init__
        label="Vendor",
    )
    version = django_filters.ChoiceFilter(
        choices=[],  # Populated dynamically in __init__
        label="Version",
    )

    def __init__(self, *args, **kwargs):
        """
        Override initializer to dynamically set the user choices
        based on distinct users currently owning jobs.
        """
        super().__init__(*args, **kwargs)
        queryset = NodeTemplate.objects.all()
        # Ottieni valori distinti
        extras = queryset.order_by("extra").values_list("extra", flat=True).distinct()
        oses = queryset.order_by("os").values_list("os", flat=True).distinct()
        usernames = (
            queryset.order_by("username").values_list("username", flat=True).distinct()
        )
        vendors = (
            queryset.order_by("vendor").values_list("vendor", flat=True).distinct()
        )
        versions = (
            queryset.order_by("version").values_list("version", flat=True).distinct()
        )

        # Aggiorna direttamente i choices del widget
        self.filters["extra"].field.choices = [(e, e) for e in extras]
        self.filters["os"].field.choices = [(o, o) for o in oses]
        self.filters["username"].field.choices = [(u, u) for u in usernames]
        self.filters["vendor"].field.choices = [(v, v) for v in vendors]
        self.filters["version"].field.choices = [(v, v) for v in versions]

    class Meta:
        model = NodeTemplate
        fields = ["vendor", "os", "version", "extra", "username"]
