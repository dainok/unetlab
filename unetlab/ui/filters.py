import django_filters
from django.db.models import Q

class BaseSearchFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    search_fields = []

    def filter_search(self, queryset, name, value):
        if not self.search_fields:
            return queryset
        q_objects = Q()
        for field in self.search_fields:
            q_objects |= Q(**{f"{field}__icontains": value})
        return queryset.filter(q_objects)