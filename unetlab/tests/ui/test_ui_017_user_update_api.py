"""Test DRF (API) user update."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_user_update_api_admin(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user update by admin."""
    user = user_set_group_multiple['admin1']
    token, _ = Token.objects.get_or_create(user=user)
    headers = {'Authorization': f'Token {token}'}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile update tested in profile tests
            continue
        url = reverse('user-detail', kwargs={'pk': u.id})
        payload = {'first_name': f'First {u.username} Name'}
        response = api_client.patch(url, payload, format='json', headers=headers)
        # Verify the response
        assert response.status_code == 200, (
            f'Failed updating {u.username} by {user.username}'
        )
        assert response.data['first_name'] == payload['first_name'], (
            f'Unexpected value for {u.username}'
        )
        # Verify the database
        target_user = User.objects.get(username=u.username)
        assert target_user.first_name == payload['first_name'], (
            f'User {target_user.username} has not been updated by {user.username}'
        )


@pytest.mark.django_db
def test_ui_user_update_api_staff(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user update by staffs."""
    user = user_set_group_multiple['staff1']
    token, _ = Token.objects.get_or_create(user=user)
    headers = {'Authorization': f'Token {token}'}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile update tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list('id', flat=True)
            & u.groups.values_list('id', flat=True)
        )
        url = reverse('user-detail', kwargs={'pk': u.id})
        payload = {'first_name': f'First {u.username} Name'}
        response = api_client.patch(url, payload, format='json', headers=headers)
        if shared_groups and (u.is_superuser or u.is_staff):
            assert response.status_code == 403, (
                f'User {u.username} must not be updated by {user.username}'
            )
        elif shared_groups:
            assert response.status_code == 200, (
                f'Failed updating {u.username} by {user.username}'
            )
            assert response.data['first_name'] == payload['first_name'], (
                f'Unexpected value for {u.username}'
            )
        else:
            assert response.status_code == 404, (
                f'User {u.username} must not be updated by {user.username}'
            )


@pytest.mark.django_db
def test_ui_user_update_api_user(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user update view by users."""
    user = user_set_group_multiple['user1']
    token, _ = Token.objects.get_or_create(user=user)
    headers = {'Authorization': f'Token {token}'}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile update tested in profile tests
            continue
        payload = {'first_name': f'First {u.username} Name'}
        shared_groups = bool(
            user.groups.values_list('id', flat=True)
            & u.groups.values_list('id', flat=True)
        )
        url = reverse('user-detail', kwargs={'pk': u.id})
        response = api_client.patch(url, payload, headers=headers)
        if shared_groups:
            assert response.status_code == 403, (
                f'User {u.username} must not be update by {user.username}'
            )
        else:
            assert response.status_code == 404, (
                f'User {u.username} must not be updated by {user.username}'
            )


@pytest.mark.django_db
def test_ui_user_update_api_guest(api_client, user_set_group1):
    """Test DRF (API) user update by guest user."""
    for u in User.objects.all():
        url = reverse('user_update', kwargs={'pk': u.id})
        payload = {'username': u.username, 'first_name': f'First {u.username} Name'}
        response = api_client.patch(url, payload, format='json')
        assert response.status_code == 302, (
            'Expected 302 (redirect to login) for guest user'
        )


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_user_update_api_role(api_client, user_set_group1, role):
    """Test DRF (API) role upgrade."""
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {'Authorization': f'Token {token}'}
    for u in User.objects.exclude(is_superuser=True):
        payload = {'is_superuser': True, 'is_staff': True}
        url = reverse('user-detail', kwargs={'pk': u.id})
        api_client.patch(url, payload, format='json', headers=headers)
        u.refresh_from_db()
        if role == 'admin' and not u.is_superuser:
            # Admins can upgrade staff/users
            assert u.is_superuser, f'Failed upgrading {u.username} by {user.username}'
        if role in ('staff', 'user'):
            # Staff/Users cannot upgrade anyone
            assert not u.is_superuser, (
                f'User {u.username} cannot be upgraded by {user.username}'
            )


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_user_update_api_groups(api_client, user_set_group1, role):
    """Test DRF (API) groups change."""
    new_group, _ = Group.objects.get_or_create(name='group_new')
    user = user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {'Authorization': f'Token {token}'}
    for u in User.objects.all():
        group_ids = set(u.groups.all().values_list('id', flat=True))
        payload = {'groups': list(group_ids) + [new_group.id]}
        url = reverse('user-detail', kwargs={'pk': u.id})
        api_client.patch(url, payload, format='json', headers=headers)
        v = User.objects.get(id=u.id)
        new_group_ids = set(v.groups.all().values_list('id', flat=True))
        if role == 'admin' and not u.is_superuser:
            # Admins can upgrade users
            v = User.objects.get(id=u.id)
            assert set(payload['groups']) == new_group_ids, (
                f'Failed upgrading {u.username} by {user.username}'
            )
        if role in ('staff', 'user'):
            # Staff cannot upgrade users
            assert group_ids == new_group_ids, (
                f'User {u.username} cannot be upgraded by {user.username}'
            )
