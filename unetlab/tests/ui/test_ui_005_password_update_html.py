"""Test HTML (UI) password update."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_password_update_html_user(
    client, user_set_group1, user_set_ungrouped, role
):
    """Test HTML (UI) user password update."""
    for user_set_group in [user_set_group1, user_set_ungrouped]:
        user = user_set_group[role]
        client.force_login(user)
        url = reverse('user_update', kwargs={'pk': user.id})
        new_password = f'{user.username}123_new'
        payload = {
            'username': user.username,
            'is_active': 'on',
            'password1': new_password,
            'password2': new_password,
        }
        response = client.post(url, payload, format='json')
        assert response.status_code == 302, (
            f'Expected 302 (redirect to login page) for user {user.username} ({role})'
        )
        # Verify the change
        user.refresh_from_db()
        assert user.check_password(new_password)
        # Check login
        logged = client.login(username=user.username, password=new_password)
        assert logged is True, f'Failed for user {user.username} ({role})'
