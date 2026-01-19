"""Test HTML (UI) lab creation."""

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from lab.models import Lab


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_lab_lab_create_html_user(client, _user_set_group1, role):
    """Test HTML (UI) lab creation."""
    user = _user_set_group1[role]
    client.force_login(user)
    url = reverse('lab_create')

    # Lab not shared
    payload = {'name': 'New private Lab'}
    response = client.post(url, payload, format='json')
    assert response.status_code == 302, (
        f'Expected 302 (redirect to list page) for user {user.username} ({role})'
    )
    assert len(Lab.objects.filter(name=payload['name'])) == 1, (
        'Lab has not been created'
    )
    assert not Lab.objects.get(name=payload['name']).shared_group, 'Lab has a group ID'

    # Shared Lab
    payload = {
        'name': 'New shared Lab',
        'shared_group': user.groups.first().id,
    }
    response = client.post(url, payload, format='json')
    assert response.status_code == 302, (
        f'Expected 302 (redirect to list page) for user {user.username} ({role})'
    )
    assert len(Lab.objects.filter(name=payload['name'])) == 1, (
        'Lab has not been created'
    )
    assert Lab.objects.get(name=payload['name']).user.id == user.id, (
        'Lab has a wrong user ID'
    )
    assert (
        Lab.objects.get(name=payload['name']).shared_group.id == payload['shared_group']
    ), 'Lab has a wrong group ID'

    # Shared Lab to an external group
    external_group = Group.objects.create(name='External Group')
    payload = {
        'name': 'New public Lab',
        'shared_group': external_group.id,
    }
    response = client.post(url, payload, format='json')
    if role == 'admin':
        assert response.status_code == 302, (
            f'Expected 302 (redirect to list page) for user {user.username} ({role})'
        )
        assert len(Lab.objects.filter(name=payload['name'])) == 1, (
            'Lab has not been created'
        )
        assert Lab.objects.get(name=payload['name']).user.id == user.id, (
            'Lab has a wrong user ID'
        )
        assert (
            Lab.objects.get(name=payload['name']).shared_group.id
            == payload['shared_group']
        ), 'Lab has a wrong group ID'
    else:
        assert response.status_code == 403, f'Failed for user {user.username}'
        assert len(Lab.objects.filter(name=payload['name'])) == 0, (
            'Lab has not been created'
        )


@pytest.mark.django_db
def test_lab_lab_create_html_guest(client):
    """Test HTML (UI) lab creation by guest user."""
    url = reverse('lab_create')
    payload = {'name': 'New Lab'}
    response = client.post(url, payload, format='json')
    assert response.status_code == 302, (
        'Expected 302 (redirect to login page) for guest user'
    )
    assert len(Lab.objects.filter(name=payload['name'])) == 0, 'Lab has been created'
