"""Test HTML (UI) user deletion."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_ui_user_delete_html_admin(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) user deletion by admin."""
    user = user_set_group_multiple['admin1']
    client.force_login(user)
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        url = reverse('user_delete', kwargs={'pk': u.id})
        response = client.get(url)
        assert response.status_code == 200, f'Expected 200 for user {user.username}'
        assert 'Are you sure' in response.text, (
            f'Expected confirmation page for user {user.username})'
        )
        response = client.post(url)
        assert response.status_code == 302, (
            f'Expected 302 (redirect to list page) for user {user.username}'
        )
        # Verify the profile has been deleted
        assert len(User.objects.filter(username=u.username)) == 0, (
            f'User {u.username} has not been deleted by {user.username}'
        )


@pytest.mark.django_db
def test_ui_user_delete_html_staff(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) user deletion by staffs."""
    user = user_set_group_multiple['staff1']
    client.force_login(user)
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list('id', flat=True)
            & u.groups.values_list('id', flat=True)
        )
        url = reverse('user_delete', kwargs={'pk': u.id})
        response = client.get(url)
        if shared_groups and (u.is_superuser or u.is_staff):
            assert response.status_code == 200, f'Expected 200 for user {user.username}'
            assert 'Are you sure' in response.text, (
                f'Expected confirmation page for user {user.username})'
            )
            response = client.post(url)
            assert response.status_code == 403, f'Expected 403 for user {user.username}'
            # Verify the profile has not been deleted
            assert len(User.objects.filter(username=u.username)) == 1, (
                f'User {u.username} must not be deleted by {user.username}'
            )
        elif shared_groups:
            assert response.status_code == 200, f'Expected 200 for user {user.username}'
            assert 'Are you sure' in response.text, (
                f'Expected confirmation page for user {user.username})'
            )
            response = client.post(url)
            assert response.status_code == 302, (
                f'Expected 302 (redirect to list page) for user {user.username}'
            )
            # Verify the profile has been deleted
            assert len(User.objects.filter(username=u.username)) == 0, (
                f'User {u.username} must be deleted by {user.username}'
            )
        else:
            assert response.status_code == 404, (
                f'User {u.username} must not be deleted by {user.username}'
            )
            assert len(User.objects.filter(id=u.id)) == 1, (
                f'User {u.username} has been deleted'
            )


@pytest.mark.django_db
def test_ui_user_delete_html_user(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) user deletion by users."""
    user = user_set_group_multiple['user1']
    client.force_login(user)
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list('id', flat=True)
            & u.groups.values_list('id', flat=True)
        )
        url = reverse('user_delete', kwargs={'pk': u.id})
        response = client.get(url)
        if shared_groups:
            assert response.status_code == 200, f'Expected 200 for user {user.username}'
            assert 'Are you sure' in response.text, (
                f'Expected confirmation page for user {user.username})'
            )
            response = client.post(url)
            assert response.status_code == 403, f'Expected 403 for user {user.username}'
            # Verify the profile has not been deleted
            assert len(User.objects.filter(username=u.username)) == 1, (
                f'User {u.username} must not be deleted by {user.username}'
            )
        else:
            assert response.status_code == 404, (
                f'User {u.username} must not be deleted by {user.username}'
            )
            assert len(User.objects.filter(id=u.id)) == 1, (
                f'User {u.username} has been deleted'
            )


@pytest.mark.django_db
def test_ui_user_delete_html_guest(client, user_set_group1):
    """Test HTML (UI) user deletion by guest user."""
    for u in User.objects.all():
        url = reverse('user_delete', kwargs={'pk': u.id})
        response = client.get(url)
        assert response.status_code == 302, 'Expected 302 (redirect to list page)'
