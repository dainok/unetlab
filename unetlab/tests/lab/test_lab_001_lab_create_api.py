"""Test DRF (API) lab creation."""

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.authtoken.models import Token
from lab.models import Lab


@pytest.mark.django_db
@pytest.mark.parametrize('role', ['admin', 'staff', 'user'])
def test_lab_lab_create_api_user(api_client, _user_set_group1, role):
    """Test DRS (API) lab creation."""
    user = _user_set_group1[role]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {'Authorization': f'Token {token}'}
    url = reverse('lab-list')

    # Lab not shared
    payload = {'name': 'New private Lab'}
    response = api_client.post(url, payload, format='json', headers=headers)
    assert response.status_code == 201, f'Failed for user {user.username}'
    assert response.data['name'] == payload['name'], 'Lab not in the returning payload'
    assert len(Lab.objects.filter(name=payload['name'])) == 1, (
        'Lab has not been created'
    )
    assert not Lab.objects.get(name=payload['name']).shared_group, 'Lab has a group ID'

    # Shared Lab
    payload = {
        'name': 'New shared Lab',
        'shared_group': user.groups.first().id,
    }
    response = api_client.post(url, payload, format='json', headers=headers)
    assert response.status_code == 201, f'Failed for user {user.username}'
    assert response.data['name'] == payload['name'], 'Lab not in the returning payload'
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
    response = api_client.post(url, payload, format='json', headers=headers)
    if role == 'admin':
        assert response.status_code == 201, f'Failed for user {user.username}'
        assert response.data['name'] == payload['name'], (
            'Lab not in the returning payload'
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
def test_lab_lab_create_api_guest(api_client):
    """Test DRS (API) lab creation by guest user."""
    url = reverse('lab-list')
    payload = {'name': 'New Lab'}
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 401, 'Expected 401 for guest user'
    assert len(Lab.objects.filter(name=payload['name'])) == 0, 'Lab has been created'
