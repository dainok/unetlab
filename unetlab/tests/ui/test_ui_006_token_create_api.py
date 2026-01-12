"""Test DRF (API) token creation."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_authentication_token_create_api_user(api_client, user_set_group1, role):
    """Test DRF (API) user token creation."""
    user = user_set_group1[role]
    password = f'{user.username}123'
    url = reverse('api_token')
    data = {'username': user.username, 'password': password}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200, f'Failed for user {user.username} ({role})'
    assert len(response.data['token']) > 0, (
        f'Missing token for user {user.username} ({role})'
    )


@pytest.mark.django_db
def test_ui_authentication_token_create_api_guest(api_client):
    """Test DRF (API) guest token creation."""
    url = reverse('api_token')
    data = {'username': 'guest', 'password': 'guest123'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 400, 'Expected 400 for guest user'
