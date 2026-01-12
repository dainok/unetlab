"""Test HTML (UI) authentication."""

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_authentication_html_user(client, user_set_group1, role):
    """Test HTML (UI) user authentication."""
    user = user_set_group1[role]
    username = user.username
    password = f'{username}123'
    logged = client.login(username=username, password=password)
    assert logged is True, f'Failed for user {username} ({role})'


@pytest.mark.django_db
def test_ui_authentication_html_guest(client):
    """Test HTML (UI) guest authentication."""
    logged = client.login(username='guest', password='guest123')
    assert logged is False, 'Expected False for guest user'
