"""Test DRF (API) group deletion."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_group_delete_api_admin(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) group deletion by admin."""
    user = user_set_group_multiple['admin1']
    token, _ = Token.objects.get_or_create(user=user)
    headers = {'Authorization': f'Token {token}'}
    for g in Group.objects.all():
        url = reverse('group-detail', kwargs={'pk': g.id})
        response = api_client.delete(url, headers=headers)
        assert response.status_code == 204, (
            f'Group {g.name} not found by {user.username}'
        )
        assert len(Group.objects.filter(id=g.id)) == 0, (
            f'Group {g.name} has not been deleted by {user.username}'
        )


@pytest.mark.django_db
def test_ui_group_delete_api_user(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) group deletion by staffs/users."""
    for user in User.objects.filter(is_superuser=False):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {'Authorization': f'Token {token}'}
        user_group_ids = list(user.groups.all().values_list('id', flat=True))
        for g in Group.objects.all():
            url = reverse('group-detail', kwargs={'pk': g.id})
            response = api_client.delete(url, headers=headers)
            if g.id in user_group_ids:
                assert response.status_code == 403, (
                    f'Group {g.name} must not be deleted by {user.username}'
                )
            else:
                assert response.status_code == 404, (
                    f'Group {g.name} must not be found by {user.username}'
                )
            assert len(Group.objects.filter(id=g.id)) == 1, (
                f'Group {g.name} has been deleted'
            )


@pytest.mark.django_db
def test_ui_group_delete_api_guest(api_client, user_set_group1):
    """Test DRS (API) group deletion by guest user."""
    for g in Group.objects.all():
        url = reverse('group-detail', kwargs={'pk': g.id})
        response = api_client.delete(url)
        assert response.status_code == 401, 'Expected 401 for guest user'
