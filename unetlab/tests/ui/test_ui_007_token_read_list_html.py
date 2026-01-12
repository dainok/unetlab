"""Test HTML (UI) token list view."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_authentication_token_read_list_html_user(client, user_set_group1, role):
    """Test HTML (UI) user token list."""
    for user in user_set_group1.values():
        Token.objects.get_or_create(user=user)
    user = user_set_group1[role]
    client.force_login(user)
    url = reverse('token_list')
    response = client.get(url)
    assert response.status_code == 200, f'Failed for user {user.username} ({role})'
    if role == 'admin':
        for token in Token.objects.all():
            assert token.key in response.text, (
                f'User {user.username} ({role}) cannot see token for user {token.user.username}'
            )
    else:
        assert Token.objects.get(user__id=user.id).key in response.text, (
            f'User {user.username} ({role}) cannot see its own token'
        )
        for token in Token.objects.exclude(user__id=user.id):
            assert token.key not in response.text, (
                f'User {user.username} ({role}) must not see token for user {token.user.username}'
            )


@pytest.mark.django_db
def test_ui_authentication_token_read_list_html_guest(client):
    """Test HTML (UI) guest token list."""
    url = reverse('token_list')
    response = client.get(url)
    assert response.status_code == 302, 'Expected 302 for guest user'
    assert response.headers['Location'] == '/accounts/login/', (
        'Expected redirect to login page for guest user'
    )
