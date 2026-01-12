"""Test HTML (UI) group deletion."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse


@pytest.mark.django_db
def test_ui_group_delete_html_admin(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) group deletion by admin."""
    user = user_set_group_multiple['admin1']
    client.force_login(user)
    for g in Group.objects.all():
        url = reverse('group_delete', kwargs={'pk': g.id})
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
        assert len(Group.objects.filter(id=g.id)) == 0, (
            f'Group {g.name} has not been deleted by {user.username}'
        )


@pytest.mark.django_db
def test_ui_group_delete_html_staff(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) group deletion by staffs/sers."""
    for user in User.objects.filter(is_superuser=False):
        client.force_login(user)
        for g in Group.objects.all():
            url = reverse('group_delete', kwargs={'pk': g.id})
            response = client.get(url)
            if user.groups.filter(id=g.id):
                assert response.status_code == 200, (
                    f'Expected 200 for user {user.username}'
                )
                assert 'Are you sure' in response.text, (
                    f'Expected confirmation page for user {user.username})'
                )
                response = client.post(url)
                assert response.status_code == 403, (
                    f'Expected 403 for user {user.username}'
                )
                # Verify the profile has not been deleted
                assert len(Group.objects.filter(id=g.id)) == 1, (
                    f'Group {g.name} must not be deleted by {user.username}'
                )
            else:
                assert response.status_code == 404, (
                    f'User {g.name} must not be deleted by {user.username}'
                )
                assert len(User.objects.filter(id=g.id)) == 1, (
                    f'Group {g.name} has been deleted'
                )


@pytest.mark.django_db
def test_ui_group_delete_html_guest(client, user_set_group1):
    """Test HTML (UI) group deletion by guest user."""
    for g in Group.objects.all():
        url = reverse('group_delete', kwargs={'pk': g.id})
        response = client.get(url)
        assert response.status_code == 302, 'Expected 302 (redirect to list page)'
