"""Test DRF (API) user list."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_user_read_list_api_admin(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user list view by admin."""
    for user in User.objects.filter(is_superuser=True):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {'Authorization': f'Token {token}'}
        all_users = list(User.objects.all().values_list('username', flat=True))
        url = reverse('user-list') + f'?per_page={len(all_users)}'
        response = api_client.get(url, headers=headers)
        assert response.status_code == 200, f'Failed for user {user.username}'
        result_users = [u['username'] for u in response.data['results']]
        for u in all_users:
            assert u in result_users, f'User {u} not found by {user.username}'


@pytest.mark.django_db
def test_ui_user_read_list_api_user(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user list view by staffs and users."""
    for user in User.objects.filter(is_superuser=False):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {'Authorization': f'Token {token}'}
        all_users = User.objects.all()
        url = reverse('user-list') + f'?per_page={len(all_users)}'
        response = api_client.get(url, headers=headers)
        assert response.status_code == 200, f'Failed for user {user.username}'
        result_users = [u['username'] for u in response.data['results']]
        # Testing users with a shared group
        all_users_w_shared_group = list(
            all_users.filter(groups__in=user.groups.all())
            .distinct()
            .values_list('username', flat=True)
        )
        for u in all_users_w_shared_group:
            assert u in result_users, f'User {u} not found by {user.username}'
        # Testing users without a shared group
        all_users_wo_shared_group = list(
            all_users.exclude(
                username__in=all_users_w_shared_group + [user.username]
            ).values_list('username', flat=True)
        )
        for u in all_users_wo_shared_group:
            assert u not in result_users, f'User {user.username} must not see {u}'


@pytest.mark.django_db
def test_ui_user_read_list_api_guest(api_client):
    """Test DRS (API) user list view by guest user."""
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == 401, 'Expected 401 for guest user'
