"""Test HTML (UI) profile view."""

from bs4 import BeautifulSoup
import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_ui_profile_read_html_user(client, user_set_group1, user_set_ungrouped, role):
    """Test HTML (UI) user profile view."""
    for user_set_group in [user_set_group1, user_set_ungrouped]:
        user = user_set_group[role]
        client.force_login(user)
        url = reverse('user_detail', kwargs={'pk': user.id})
        response = client.get(url)
        assert response.status_code == 200, f'Failed for user {user.username} ({role})'
        # Verify the page content
        html = response.content.decode()
        soup = BeautifulSoup(html, 'html.parser')
        card_bodies = soup.find_all('div', class_='card-body')
        assert any(user.username in div.get_text(strip=True) for div in card_bodies), (
            f'Profile not found for {role}'
        )
