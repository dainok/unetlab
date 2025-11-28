"""Test DRF (API) authentication."""

import base64
import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_authentication_api_password(api_client, user_set_group1, role):
    """Test DRF (API) password authentication."""
    user = user_set_group1[role]
    userpass = f"{user.username}:{user.username}123"
    token = base64.b64encode(userpass.encode()).decode()
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {token}")
    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code == 401, "Expected 401 for password authentication"


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_authentication_api_token(api_client, user_set_group1, role):
    """Test DRF (API) token authentication."""
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("user-list")
    response = api_client.get(url, headers=headers)
    assert response.status_code == 200, f"Failed for user {user.username} ({role})"


@pytest.mark.django_db
def test_ui_authentication_api_guest(api_client):
    """Test DRF (API) guest authentication."""
    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code == 401, "Expected 401 for guest user"
