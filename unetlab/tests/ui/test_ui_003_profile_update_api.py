"""Test DRF (API) profile update."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_profile_update_api_user(
    api_client, user_set_group1, user_set_ungrouped, role
):
    """Test DRF (API) user profile update."""
    for user_set_group in [user_set_group1, user_set_ungrouped]:
        user = user_set_group[role]
        token, _ = Token.objects.get_or_create(user=user)
        headers = {'Authorization': f'Token {token}'}
        url = reverse('user-detail', kwargs={'pk': user.id})
        payload = {'first_name': f'New {user.username} Name'}
        response = api_client.patch(url, payload, headers=headers, format='json')
        assert response.status_code == 200, f'Failed for user {user.username} ({role})'
        assert response.data['first_name'] == payload['first_name'], (
            f'First name not found for user {user.username} ({role})'
        )
