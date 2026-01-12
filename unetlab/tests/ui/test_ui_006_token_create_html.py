"""Test HTML (UI) token creation."""

from rest_framework.authtoken.models import Token
import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_authentication_token_create_html_user(client, user_set_group1, role):
    """Test HTML (UI) user token creation."""
    user = user_set_group1[role]
    client.force_login(user)
    url = reverse('token_create')
    response = client.post(url)
    assert response.status_code == 302, (
        f'Expected 302 (redirect to list page) for user {user.username} ({role})'
    )
    assert len(Token.objects.filter(user_id=user.id)) == 1, (
        f'Token not found for user {user.username} ({role})'
    )


@pytest.mark.django_db
def test_ui_authentication_token_create_html_guest(client):
    """Test HTML (UI) guest token creation."""
    url = reverse('token_create')
    response = client.post(url)
    assert response.status_code == 401, 'Expected 401 for guest user'
