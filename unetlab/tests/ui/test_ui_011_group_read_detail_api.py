"""Test DRF (API) group view."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_group_read_detail_api_admin(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) group detail view by admin."""
    for user in User.objects.filter(is_superuser=True):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token}"}
        for g in Group.objects.all():
            url = reverse("group-detail", kwargs={"pk": g.id})
            response = api_client.get(url, headers=headers)
            assert (
                response.status_code == 200
            ), f"Group {g.name} not found by {user.username}"


@pytest.mark.django_db
def test_ui_group_read_detail_api_user(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) group detail view by staffs and users."""
    for user in User.objects.filter(is_superuser=False):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token}"}
        # Testing user groups
        user_group_ids = user.groups.all().values_list("id", flat=True)
        for g in user_group_ids:
            url = reverse("group-detail", kwargs={"pk": g})
            response = api_client.get(url, headers=headers)
            assert (
                response.status_code == 200
            ), f"Group {g.name} not found by {user.username}"
        # Testing other groups
        other_groups = Group.objects.exclude(id__in=user_group_ids)
        for g in other_groups:
            url = reverse("group-detail", kwargs={"pk": g})
            response = api_client.get(url, headers=headers)
            assert response.status_code == 404, f"User {user.username} must not see {g}"


@pytest.mark.django_db
def test_ui_group_read_detail_api_guest(api_client, user_set_group1):
    """Test DRS (API) group detail view by guest user."""
    for g in Group.objects.all():
        url = reverse("group-detail", kwargs={"pk": g.id})
        response = api_client.get(url)
        assert response.status_code == 401, "Expected 401 for guest user"
