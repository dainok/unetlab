"""Test DRF (API) user creation."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_user_create_api_user(api_client, user_set_group1, role):
    """Test DRS (API) user creation."""
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-list")
    payload = {"username": "new_user"}
    response = api_client.post(url, payload, format="json", headers=headers)
    if role == "admin":
        # Admin users must be able to create new users.
        assert response.status_code == 201, f"Failed for user {user.username}"
        assert (
            response.data["username"] == payload["username"]
        ), "Username not in the returning payload"
        assert (
            len(User.objects.filter(username=payload["username"])) == 1
        ), "User has not been created"
    else:
        # Non admin users cannot create new users.
        assert response.status_code == 403, f"Expected 401 for {user.username}"
        assert (
            len(User.objects.filter(username=payload["username"])) == 0
        ), "User has been created"


@pytest.mark.django_db
def test_ui_user_create_api_guest(api_client):
    """Test DRS (API) get user creation by guest user."""
    url = reverse("user-list")
    payload = {"username": "new_user"}
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 401, "Expected 401 for guest user"
    assert (
        len(User.objects.filter(username=payload["username"])) == 0
    ), "User has been created"
