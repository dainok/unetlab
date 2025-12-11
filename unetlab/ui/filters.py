"""Filter definitions for UI app."""

from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
import django_filters
from rest_framework.authtoken.models import Token
from ui.include.filters import SearchFilterSet


CHOICES_YES_NO = [
    ("", "---------"),
    (True, _("Yes")),
    (False, _("No")),
]


#############################################################################
# Group
#############################################################################


class GroupFilter(SearchFilterSet):
    """Filter class for the Group model."""

    search_fields = ["name"]


#############################################################################
# User
#############################################################################


class UserFilter(SearchFilterSet):
    """Filter class for the User model."""

    search_fields = ["username", "first_name", "last_name", "email"]
    is_active = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=CHOICES_YES_NO,
        ),
        label=_("Active users"),
    )
    is_staff = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=CHOICES_YES_NO,
        ),
        label=_("Staff users"),
    )
    is_superuser = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=CHOICES_YES_NO,
        ),
        label=_("Admin users"),
    )
    last_login_before = django_filters.DateFilter(
        field_name="last_login",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Last login before"),
    )
    last_login_after = django_filters.DateFilter(
        field_name="last_login",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Last login after"),
    )

    class Meta:
        """Meta options."""

        fields = ["groups", "is_active", "is_superuser", "is_staff"]
        model = User

    def __init__(self, *args, **kwargs):
        """Populate group filter based on the user role."""
        super().__init__(*args, **kwargs)

        if self.request:
            user = self.request.user
            if user.is_superuser:
                # Admins can see all groups
                qs = Group.objects.all().order_by("name")
            else:
                qs = user.groups.all().order_by("name")
            self.filters["groups"].field.queryset = qs


#############################################################################
# Token
#############################################################################


class TokenFilter(SearchFilterSet):
    """Filter class for the Token model."""

    user__is_active = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=CHOICES_YES_NO,
        ),
        label=_("Active users"),
    )
    user__is_staff = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=CHOICES_YES_NO,
        ),
        label=_("Staff users"),
    )
    user__is_superuser = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=CHOICES_YES_NO,
        ),
        label=_("Admin users"),
    )

    class Meta:
        """Meta options."""

        fields = ["user__is_active", "user__is_superuser", "user__is_staff"]
        model = Token
