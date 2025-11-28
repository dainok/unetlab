"""Test HTML (UI) profile deletion."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_ui_profile_delete_html_admin(client, user_set_group1, user_set_ungrouped):
    """Test HTML (UI) admin profile deletion."""
    for user_set_group in [user_set_group1, user_set_ungrouped]:
        role = "admin"
        user = user_set_group[role]
        client.force_login(user)
        url = reverse("user_delete", kwargs={"pk": user.id})
        response = client.get(url)
        assert (
            response.status_code == 200
        ), f"Expected 200 for user {user.username} ({role})"
        assert (
            "Are you sure" in response.text
        ), f"Expected confirmation page for user {user.username} ({role})"
        response = client.post(url)
        assert (
            response.status_code == 403
        ), f"Expected 403 for user {user.username} ({role})"
        # Verify the profile still exists
        assert (
            len(User.objects.filter(username=user.username)) == 1
        ), f"Expected 200 for user {user.username} ({role})"


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["staff", "user"])
def test_ui_profile_delete_html_user(client, user_set_group1, user_set_ungrouped, role):
    """Test HTML (UI) non-admin profile deletion."""
    for user_set_group in [user_set_group1, user_set_ungrouped]:
        user = user_set_group[role]
        client.force_login(user)
        url = reverse("user_delete", kwargs={"pk": user.id})
        response = client.get(url)
        assert (
            response.status_code == 200
        ), f"Expected 200 for user {user.username} ({role})"
        assert (
            "Are you sure" in response.text
        ), f"Expected confirmation page for user {user.username} ({role})"
        response = client.post(url)
        assert (
            response.status_code == 302
        ), f"Expected 302 (redirect to login page) for user {user.username} ({role})"
        # Verify the profile has been deleted
        assert (
            len(User.objects.filter(username=user.username)) == 0
        ), f"Expected 200 for user {user.username} ({role})"
