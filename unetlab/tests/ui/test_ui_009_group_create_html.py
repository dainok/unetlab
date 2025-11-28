"""Test HTML (UI) group creation."""

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_group_create_html_user(client, user_set_group1, role):
    """Test HTML (UI) group creation."""
    user = user_set_group1[role]
    client.force_login(user)
    url = reverse("group_create")
    payload = {"name": "new_group"}
    response = client.post(url, payload, format="json")
    if role == "admin":
        # Admin users must be able to create new groups.
        assert (
            response.status_code == 302
        ), f"Expected 302 (redirect to list page) for user {user.username} ({role})"
        assert (
            len(Group.objects.filter(name=payload["name"])) == 1
        ), "Group has not been created"
    else:
        # Non admin users cannot create new groups.
        assert response.status_code == 403, f"Expected 401 for {user.username}"
        assert (
            len(Group.objects.filter(name=payload["name"])) == 0
        ), "Group has been created"


@pytest.mark.django_db
def test_ui_group_create_html_guest(client):
    """Test HTML (UI) get group creation by guest user."""
    url = reverse("group_create")
    payload = {"name": "new_group"}
    response = client.post(url, payload, format="json")
    assert (
        response.status_code == 302
    ), "Expected 302 (redirect to login page) for guest user"
    assert (
        len(Group.objects.filter(name=payload["name"])) == 0
    ), "Group has been created"
