"""Test HTML (UI) token deletion."""

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_authentication_token_delete_html_user(client, user_set_group1, role):
    """Test HTML (UI) user token deletion."""
    for user in user_set_group1.values():
        Token.objects.get_or_create(user_id=user.id)
    user = user_set_group1[role]
    client.force_login(user)
    if role == 'admin':
        for token in Token.objects.all():
            # Admins can delete all tokens
            url = reverse('token_delete', kwargs={'pk': token.key})
            response = client.get(url)
            assert response.status_code == 200, (
                f'Expected 200 for user {user.username} ({role})'
            )
            assert 'Are you sure' in response.text, (
                f'Expected confirmation page for user {user.username} ({role})'
            )
            response = client.post(url)
            # Verify the token has been deleted
            assert len(Token.objects.filter(user_id=user.id)) == 0, (
                f'Token for user {user.username} ({role}) has not been deleted'
            )
    else:
        # Delete owned token
        token = Token.objects.get(user_id=user.id)
        url = reverse('token_delete', kwargs={'pk': token.key})
        response = client.get(url)
        assert response.status_code == 200, (
            f'Expected 200 for user {user.username} ({role})'
        )
        assert 'Are you sure' in response.text, (
            f'Expected confirmation page for user {user.username} ({role})'
        )
        response = client.post(url)

        # Standard users cannot delete other tokens
        for token in Token.objects.exclude(user_id=user.id):
            # Admins can delete all tokens
            url = reverse('token_delete', kwargs={'pk': token.key})
            response = client.get(url)
            assert response.status_code == 404, (
                f'Expected 404 for user {user.username} ({role})'
            )


@pytest.mark.django_db
def test_ui_authentication_token_delete_html_guest(client):
    """Test HTML (UI) guest token list view."""
    url = reverse('token_list')
    response = client.get(url)
    assert response.status_code == 302, 'Expected 302 for guest user'
    assert response.headers['Location'] == '/accounts/login/', (
        'Expected redirect to login page for guest user'
    )
