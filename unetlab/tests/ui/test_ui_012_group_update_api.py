"""Test DRF (API) group update."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_group_update_api_admin(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) group update by admin."""
    user = user_set_group_multiple["admin1"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    for g in Group.objects.all():
        url = reverse("group-detail", kwargs={"pk": g.id})
        payload = {"name": f"New {g.name} Name"}
        response = api_client.patch(url, payload, format="json", headers=headers)
        # Verify the response
        assert (
            response.status_code == 200
        ), f"Failed updating {g.name} by {user.username}"
        assert (
            response.data["name"] == payload["name"]
        ), f"Unexpected value for {g.name}"
        # Verify the database
        target_group = Group.objects.get(name=payload["name"])
        assert (
            target_group.name == payload["name"]
        ), f"User {target_group.name} has not been updated by {user.username}"


@pytest.mark.django_db
def test_ui_group_update_api_user(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user detail view by users/staffs."""
    for user in User.objects.filter(is_superuser=False):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token}"}
        # Testing user groups
        user_group_ids = user.groups.all()
        for g in user_group_ids:
            url = reverse("group-detail", kwargs={"pk": g.id})
            payload = {"name": f"New {g.name} Name"}
            response = api_client.patch(url, payload, headers=headers)
            assert (
                response.status_code == 403
            ), f"Group {g.name} must not be updated by {user.username}"
        # Testing other groups
        other_groups = Group.objects.exclude(
            id__in=user_group_ids.values_list("id", flat=True)
        )
        for g in other_groups:
            url = reverse("group-detail", kwargs={"pk": g})
            payload = {"name": f"New {g.name} Name"}
            response = api_client.get(url, payload, headers=headers)
            assert response.status_code == 404, f"User {user.username} must not see {g}"


@pytest.mark.django_db
def test_ui_group_update_api_guest(client, user_set_group1):
    """Test DRF (API) group update by guest user."""
    for g in Group.objects.all():
        url = reverse("group-detail", kwargs={"pk": g.id})
        payload = {"name": f"New {g.name} Name"}
        response = client.patch(url, payload, format="json")
        assert response.status_code == 401, "Expected 403 for guest user"
