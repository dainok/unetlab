"""Generic reusable search filter for Django models."""

from django import forms
from django.db.models import Q
import django_filters


class SearchFilterSet(django_filters.FilterSet):
    """Base filter class providing a generic text search."""

    search = django_filters.CharFilter(method='filter_search')
    search_fields = []

    WIDGET_CLASSES = {
        forms.Select: 'form-select',
        forms.TextInput: 'form-control',
        forms.DateInput: 'form-control',
        forms.NumberInput: 'form-control',
        forms.CheckboxInput: 'form-check-input',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.filters.values():
            # Don't touch dynamic choices
            if isinstance(f, django_filters.ChoiceFilter):
                # Populate choices
                if getattr(f, 'extra', {}).get('choices') == [] and hasattr(
                    f, 'get_choices'
                ):
                    f.extra['choices'] = f.get_choices()

            # Apply CSS classes without touching choices
            widget = getattr(f.field, 'widget', None)
            if widget:
                existing_classes = widget.attrs.get('class', '')
                for widget_type, css_class in self.WIDGET_CLASSES.items():
                    if isinstance(widget, widget_type):
                        combined = (existing_classes + ' ' + css_class).strip()
                        widget.attrs['class'] = combined
                        break

    def filter_search(self, queryset, name, value):
        """Apply a case-insensitive `icontains` filter across all search fields."""
        if not self.search_fields:
            return queryset
        q_objects = Q()
        for field in self.search_fields:
            q_objects |= Q(**{f'{field}__icontains': value})
        return queryset.filter(q_objects)
