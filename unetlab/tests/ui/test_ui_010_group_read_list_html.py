"""Test HTML (UI) group list view."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse


@pytest.mark.django_db
def test_ui_group_read_list_html_admin(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) group list view by admin."""
    for user in User.objects.filter(is_superuser=True):
        all_groups = list(Group.objects.all().values_list("name", flat=True))
        client.force_login(user)
        url = reverse("group_list") + f"?per_page={len(all_groups)}"
        response = client.get(url)
        assert response.status_code == 200, f"Failed for user {user.username}"
        for g in all_groups:
            assert g in response.text, f"Group {g} not found by {user.username}"


@pytest.mark.django_db
def test_ui_group_read_list_html_user(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) group list view by staffs and users."""
    for user in User.objects.filter(is_superuser=False):
        all_groups = Group.objects.all()
        client.force_login(user)
        url = reverse("group_list") + f"?per_page={len(all_groups)}"
        response = client.get(url)
        assert response.status_code == 200, f"Failed for user {user.username}"
        # Testing user groups
        user_groups = user.groups.all().values_list("name", flat=True)
        for g in user_groups:
            assert g in response.text, f"Group {g} not found by {user.username}"
        # Testing other groups
        other_groups = Group.objects.exclude(name__in=user_groups).values_list(
            "name", flat=True
        )
        for g in other_groups:
            assert g not in response.text, f"User {user.username} must not see {g}"


@pytest.mark.django_db
def test_ui_group_read_list_html_guest(client):
    """Test HTML (UI) group list view by guest user."""
    url = reverse("group_list")
    response = client.get(url)
    assert (
        response.status_code == 302
    ), f"Expected 302 (redirect to login page) for guest user"
