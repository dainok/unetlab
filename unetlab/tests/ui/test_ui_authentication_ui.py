"""Test UI authentication."""

import pytest


@pytest.mark.django_db
def test_ui_authentication_ui_admin(client, admin_user):
    """Test UI authentication by admin."""
    logged = client.login(username="admin", password="admin_pass")
    assert logged is True


@pytest.mark.django_db
def test_ui_authentication_ui_staff(client, staff_user):
    """Test UI authentication by staff."""
    logged = client.login(username="staff", password="staff_pass")
    assert logged is True


@pytest.mark.django_db
def test_ui_authentication_ui_user(client, user):
    """Test UI authentication by user."""
    logged = client.login(username="user", password="user_pass")
    assert logged is True


@pytest.mark.django_db
def test_ui_authentication_ui_guest(client):
    """Test UI authentication by non-existent user."""
    logged = client.login(username="guest", password="guest_pass")
    assert logged is False


# def test_login_view(client, django_user_model):
#     username = "andrea"
#     password = "1234"
#     django_user_model.objects.create_user(username=username, password=password)
#     login = client.login(username=username, password=password)
#     assert login is True
