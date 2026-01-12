"""Test HTML (UI) constance parameter view."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_constance_read_list_html(client, user_set_group1, role):
    """Test HTML (UI) constance read by users."""
    user = user_set_group1[role]
    client.force_login(user)
    url = reverse('settings_list')
    response = client.get(url)
    if user.is_superuser:
        assert response.status_code == 200, f'Failed for user {user.username}'
    else:
        assert response.status_code == 403, (
            f'User {user.username} must not see Constance settings'
        )


@pytest.mark.django_db
def test_ui_constance_read_list_html_guest(client):
    """Test HTML (UI) constance read by guest users."""
    url = reverse('settings_list')
    response = client.get(url)
    assert response.status_code == 302, 'Expected 302 (redirect to list page)'
