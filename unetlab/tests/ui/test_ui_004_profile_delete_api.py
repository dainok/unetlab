"""Test DRF (API) profile deletion."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_profile_delete_api_admin(api_client, user_set_group1, user_set_ungrouped):
    """Test DRF (API) admin profile deletion."""
    for user_set_group in [user_set_group1, user_set_ungrouped]:
        role = 'admin'
        user = user_set_group[role]
        token, _ = Token.objects.get_or_create(user=user)
        headers = {'Authorization': f'Token {token}'}
        url = reverse('user-detail', kwargs={'pk': user.id})
        response = api_client.delete(url, headers=headers)
        assert response.status_code == 403, (
            f'Expected 403 for user {user.username} ({role})'
        )
        # Verify the profile still exists
        assert len(User.objects.filter(username=user.username)) == 1, (
            f'Expected 200 for user {user.username} ({role})'
        )


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['staff', 'user'])
def test_ui_profile_delete_api_user(
    api_client, user_set_group1, user_set_ungrouped, role
):
    """Test DRF (API) non-admin profile deletion."""
    for user_set_group in [user_set_group1, user_set_ungrouped]:
        user = user_set_group[role]
        token, _ = Token.objects.get_or_create(user=user)
        headers = {'Authorization': f'Token {token}'}
        url = reverse('user-detail', kwargs={'pk': user.id})
        response = api_client.delete(url, headers=headers)
        assert response.status_code == 204, f'Failed for user {user.username} ({role})'
        # Verify the profile has been deleted
        assert len(User.objects.filter(username=user.username)) == 0, (
            f'Expected 200 for user {user.username} ({role})'
        )
