"""Filter definitions for Job app."""

from django import forms
import django_filters
from task.models import Task, Log, LogSeverityChoices
from ui.include.filters import SearchFilterSet


#############################################################################
# Task
#############################################################################


class TaskFilter(SearchFilterSet):
    """Filter class for the Task model."""

    created_at__gte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-2'}),
        label='Created After',
    )
    created_at__lte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-2'}),
        label='Created Before',
    )

    class Meta:
        model = Task
        fields = ['user', 'status', 'created_at__gte', 'created_at__lte']


#############################################################################
# Log
#############################################################################


class LogFilter(SearchFilterSet):
    """Filter class for the Log model."""

    search_fields = ['message']
    acknowledged = django_filters.BooleanFilter(
        widget=forms.Select(
            attrs={'class': 'form-select'},
            choices=[
                ('', '---------'),
                ('true', 'Yes'),
                ('false', 'No'),
            ],
        ),
        label='Acknowledged',
    )
    severity = django_filters.ChoiceFilter(
        choices=LogSeverityChoices.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Severity',
    )
    created_at__gte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-2'}),
        label='Created After',
    )
    created_at__lte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-2'}),
        label='Created Before',
    )

    class Meta:
        model = Log
        fields = ['severity', 'acknowledged', 'created_at__gte', 'created_at__lte']
