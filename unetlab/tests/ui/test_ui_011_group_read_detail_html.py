"""Test HTML (UI) group view."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse


@pytest.mark.django_db
def test_ui_group_read_detail_html_admin(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) group detail view by admin."""
    for user in User.objects.filter(is_superuser=True):
        client.force_login(user)
        for g in Group.objects.all():
            url = reverse("group_detail", kwargs={"pk": g.id})
            response = client.get(url)
            assert (
                response.status_code == 200
            ), f"Group {g.name} not found by {user.username}"


@pytest.mark.django_db
def test_ui_group_read_detail_html_user(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) group detail view by staffs and users."""
    for user in User.objects.filter(is_superuser=False):
        client.force_login(user)
        all_users = User.objects.all()
        # Testing user groups
        user_group_ids = user.groups.all()
        for g in user_group_ids:
            url = reverse("group_detail", kwargs={"pk": g.id})
            response = client.get(url)
            assert (
                response.status_code == 200
            ), f"Group {g.name} not found by {user.username}"
        # Testing other groups
        other_groups = Group.objects.exclude(
            id__in=user_group_ids.values_list("id", flat=True)
        )
        for g in other_groups:
            url = reverse("group_detail", kwargs={"pk": g.id})
            response = client.get(url)
            assert response.status_code == 404, f"User {user.username} must not see {g}"


@pytest.mark.django_db
def test_ui_user_read_detail_html_guest(client, user_set_group1):
    """Test HTML (UI) user detail view by guest user."""
    for g in Group.objects.all():
        url = reverse("group-detail", kwargs={"pk": g.id})
        response = client.get(url)
        assert response.status_code == 401, "Expected 401 for guest user"
