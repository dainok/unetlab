"""Test HTML (UI) user creation."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_user_create_html_user(client, user_set_group1, role):
    """Test HTML (UI) user creation."""
    user = user_set_group1[role]
    client.force_login(user)
    url = reverse('user_create')
    payload = {'username': 'new_user'}
    response = client.post(url, payload, format='json')
    if role == 'admin':
        # Admin users must be able to create new users.
        assert response.status_code == 302, (
            f'Expected 302 (redirect to list page) for user {user.username} ({role})'
        )
        assert len(User.objects.filter(username=payload['username'])) == 1, (
            'User has not been created'
        )
    else:
        # Non admin users cannot create new users.
        assert response.status_code == 403, f'Expected 401 for {user.username}'
        assert len(User.objects.filter(username=payload['username'])) == 0, (
            'User has been created'
        )


@pytest.mark.django_db
def test_ui_user_create_html_guest(client):
    """Test HTML (UI) get user creation by guest user."""
    url = reverse('user_create')
    payload = {'username': 'new_user'}
    response = client.post(url, payload, format='json')
    assert response.status_code == 302, (
        'Expected 302 (redirect to login page) for guest user'
    )
    assert len(User.objects.filter(username=payload['username'])) == 0, (
        'User has been created'
    )
