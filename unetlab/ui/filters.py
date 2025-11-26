"""Filter definitions for UI app."""

from django import forms
from django.contrib.auth.models import User
import django_filters
from rest_framework.authtoken.models import Token
from ui.include.filters import SearchFilterSet
from ui.include import messages


#############################################################################
# Group
#############################################################################


class GroupFilter(SearchFilterSet):
    """Filter class for the `Group` model.

    Provides text search across group names.

    Attributes:
        search_fields (list[str]): Fields used for search; in this case, ["name"].
    """

    search_fields = ["name"]


#############################################################################
# User
#############################################################################


class UserFilter(SearchFilterSet):
    """Filter class for the `User` model.

    Extends the base search functionality with additional filters for
    common user attributes such as active status, staff/admin privileges,
    and login activity.

    Attributes:
        search_fields (list[str]): Fields used for text search ("name").
        is_active (BooleanFilter): Filter users by active status.
        is_staff (BooleanFilter): Filter users by staff membership.
        is_superuser (BooleanFilter): Filter users by superuser/admin status.
        last_login_before (DateFilter): Filter users who last logged in before a date.
        last_login_after (DateFilter): Filter users who last logged in after a date.
    """

    search_fields = ["username", "first_name", "last_name", "email"]
    is_active = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=messages.CHOICES_YES_NO,
        ),
        label=messages.FILTER_ACTIVE_USERS,
    )
    is_staff = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=messages.CHOICES_YES_NO,
        ),
        label=messages.FILTER_STAFF_USERS,
    )
    is_superuser = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=messages.CHOICES_YES_NO,
        ),
        label=messages.FILTER_ADMIN_USERS,
    )
    last_login_before = django_filters.DateFilter(
        field_name="last_login",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label=messages.FILTER_LOGGED_BEFORE,
    )
    last_login_after = django_filters.DateFilter(
        field_name="last_login",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
        label=messages.FILTER_LOGGED_AFTER,
    )

    class Meta:
        """Meta configuration for `UserFilter`.

        Attributes:
            model (User): The model to filter.
            fields (list[str]): List of filterable fields.
        """

        model = User
        fields = ["is_active", "is_superuser", "is_staff"]


#############################################################################
# Token
#############################################################################


class TokenFilter(SearchFilterSet):
    """Filter class for the `Token` model.

    Extends the base search functionality with additional filters for
    common user attributes such as active status, staff/admin privileges,
    and login activity.
    """

    user__is_active = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=messages.CHOICES_YES_NO,
        ),
        label=messages.FILTER_ACTIVE_USERS,
    )
    user__is_staff = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=messages.CHOICES_YES_NO,
        ),
        label=messages.FILTER_STAFF_USERS,
    )
    user__is_superuser = django_filters.BooleanFilter(
        widget=forms.Select(
            choices=messages.CHOICES_YES_NO,
        ),
        label=messages.FILTER_ADMIN_USERS,
    )

    class Meta:
        """Meta configuration for `TokenFilter`.

        Attributes:
            model (Token): The model to filter.
            fields (list[str]): List of filterable fields.
        """

        model = Token
        fields = ["user__is_active", "user__is_superuser", "user__is_staff"]
