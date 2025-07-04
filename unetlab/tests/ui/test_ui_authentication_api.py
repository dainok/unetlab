"""Test API authentication."""

from django.urls import reverse


def test_ui_authentication_api_token_admin(api_client, admin_user):
    """Test API authentication by admin."""
    url = reverse("api_token")
    data = {"username": "admin", "password": "admin_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert "token" in response.data
    assert len(response.data["token"]) > 0


def test_ui_authentication_api_token_staff(api_client, staff_user):
    """Test API authentication by staff."""
    url = reverse("api_token")
    data = {"username": "staff", "password": "staff_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert "token" in response.data
    assert len(response.data["token"]) > 0


def test_ui_authentication_api_token_user(api_client, user):
    """Test API authentication by user."""
    url = reverse("api_token")
    data = {"username": "user", "password": "user_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert "token" in response.data
    assert len(response.data["token"]) > 0


def test_ui_authentication_api_token_guest(api_client, db):
    """Test UI authentication by non-existent user."""
    url = reverse("api_token")
    data = {"username": "guest", "password": "guest_pass"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
