"""Generic reusable search filter for Django models.

This filter extends `django_filters.FilterSet` and allows subclasses
to define a list of searchable fields via `search_fields`.
"""

from django import forms
from django.db.models import Q
import django_filters


class SearchFilterSet(django_filters.FilterSet):
    """Base filter class providing a generic text search.

    Subclasses must define `search_fields` as a list of model fields
    that should be included in the search.
    """

    search = django_filters.CharFilter(method="filter_search")
    search_fields = []

    WIDGET_CLASSES = {
        forms.Select: "form-select",
        forms.TextInput: "form-control",
        forms.DateInput: "form-control",
        forms.NumberInput: "form-control",
        forms.CheckboxInput: "form-check-input",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.filters.values():
            # Se il filtro ha choices dinamici, non li tocchiamo
            if isinstance(f, django_filters.ChoiceFilter):
                # Se non sono già popolati, prova a richiamare il metodo per popolarli
                if getattr(f, "extra", {}).get("choices") == [] and hasattr(
                    f, "get_choices"
                ):
                    f.extra["choices"] = f.get_choices()

            # Applica le classi CSS al widget senza sovrascrivere i choices
            widget = getattr(f.field, "widget", None)
            if widget:
                existing_classes = widget.attrs.get("class", "")
                for widget_type, css_class in self.WIDGET_CLASSES.items():
                    if isinstance(widget, widget_type):
                        combined = (existing_classes + " " + css_class).strip()
                        widget.attrs["class"] = combined
                        break

    def filter_search(self, queryset, name, value):
        """Apply a case-insensitive `icontains` filter across all search fields.

        Args:
            queryset (QuerySet): The initial queryset to filter.
            name (str): The name of the filter field (unused).
            value (str): The search term entered by the user.

        Returns:
            QuerySet: The filtered queryset.
        """
        if not self.search_fields:
            return queryset
        q_objects = Q()
        for field in self.search_fields:
            q_objects |= Q(**{f"{field}__icontains": value})
        return queryset.filter(q_objects)
