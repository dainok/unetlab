"""Test DRF (API) group creation."""

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_group_create_api_user(api_client, user_set_group1, role):
    """Test DRS (API) group creation."""
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("group-list")
    payload = {"name": "new_group"}
    response = api_client.post(url, payload, format="json", headers=headers)
    if role == "admin":
        # Admin users must be able to create new groups.
        assert response.status_code == 201, f"Failed for user {user.username}"
        assert (
            response.data["name"] == payload["name"]
        ), f"Group not in the returning payload"
        assert (
            len(Group.objects.filter(name=payload["name"])) == 1
        ), f"Group has not been created"
    else:
        # Non admin users cannot create new groups.
        assert response.status_code == 403, f"Expected 401 for {user.username}"
        assert (
            len(Group.objects.filter(name=payload["name"])) == 0
        ), f"Group has been created"


@pytest.mark.django_db
def test_ui_group_create_api_guest(api_client):
    """Test DRS (API) get group creation by guest user."""
    url = reverse("group-list")
    payload = {"name": "new_group"}
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 401, "Expected 401 for guest user"
    assert (
        len(Group.objects.filter(name=payload["name"])) == 0
    ), f"Group has been created"
