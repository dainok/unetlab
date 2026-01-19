"""Test DRF (API) lab creation from HLD."""

import pytest
from pathlib import Path
from lab.models import Lab
from django.template.defaultfilters import slugify
from django.urls import reverse


@pytest.mark.django_db
def test_lab_lab_create_html_hld(client, _user_set_group1):
    """Test DRS (API) lab creation from HLD file."""
    user = _user_set_group1['user']
    client.force_login(user)
    url = reverse('lab_create')

    # Load HLD from file
    hld_dir = Path(__file__).parent / 'hld'
    hld_files = sorted(hld_dir.glob('hld-*.yml'))
    for hld_file in hld_files:
        with open(hld_file, encoding='utf-8') as fh:
            hld = fh.read()

        # Create the lab
        payload = {
            'name': f'Lab from {slugify(hld_file)} file',
            'hld': hld,
        }
        response = client.post(url, payload, format='json')
        assert response.status_code == 302, (
            f'Expected 302 (redirect to list page) for user {user.username}'
        )
        assert len(Lab.objects.filter(name=payload['name'])) == 1, (
            'Lab has not been created'
        )
