"""Test HTML (UI) user list view."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_ui_user_read_list_html_admin(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) user list view by admin."""
    for user in User.objects.filter(is_superuser=True):
        all_users = list(User.objects.all().values_list("username", flat=True))
        client.force_login(user)
        url = reverse("user_list") + f"?per_page={len(all_users)}"
        response = client.get(url)
        assert response.status_code == 200, f"Failed for user {user.username}"
        for u in all_users:
            assert u in response.text, f"User {u} not found by {user.username}"


@pytest.mark.django_db
def test_ui_user_read_list_html_user(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) user list view by staffs and users."""
    for user in User.objects.filter(is_superuser=False):
        all_users = User.objects.all()
        client.force_login(user)
        url = reverse("user_list") + f"?per_page={len(all_users)}"
        response = client.get(url)
        assert response.status_code == 200, f"Failed for user {user.username}"
        # Testing users with a shared group
        all_users_w_shared_group = list(
            all_users.filter(groups__in=user.groups.all())
            .distinct()
            .values_list("username", flat=True)
        )
        for u in all_users_w_shared_group:
            assert u in response.text, f"User {u} not found by {user.username}"
        # Testing users without a shared group
        all_users_wo_shared_group = list(
            all_users.exclude(
                username__in=all_users_w_shared_group + [user.username]
            ).values_list("username", flat=True)
        )
        for u in all_users_wo_shared_group:
            assert u not in response.text, f"User {user.username} must not see {u}"


@pytest.mark.django_db
def test_ui_user_read_list_html_guest(client):
    """Test HTML (UI) user list view by guest user."""
    url = reverse("user_list")
    response = client.get(url)
    assert (
        response.status_code == 302
    ), "Expected 302 (redirect to login page) for guest user"
