from django.db.models import Q
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
import django_filters


class SearchFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    search_fields = []

    def filter_search(self, queryset, name, value):
        if not self.search_fields:
            return queryset
        q_objects = Q()
        for field in self.search_fields:
            q_objects |= Q(**{f"{field}__icontains": value})
        return queryset.filter(q_objects)
