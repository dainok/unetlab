"""Test DRF (API) lab creation."""

import yaml
import json
import pytest
from pathlib import Path
from lab.models import Lab
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_lab_lab_create_api_hld(api_client, user_set_group1):
    """Test DRS (API) lab creation from HLD file."""
    user = user_set_group1["user"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    url = reverse("lab-list")

    # Load HLD from file
    hld_dir = Path(__file__).parent / "hld"
    hld_files = sorted(hld_dir.glob("hld-*.yml"))
    for hld_file in  hld_files:
        with open(hld_file, "r", encoding="utf-8") as fh:
            hld = fh.read()

        # Create the lab
        payload = {
            "name": "Lab from",
            "hld": hld,
        }
        print(payload)
        response = api_client.post(url, payload, format="json", headers=headers)
        assert response.status_code == 201, f"Failed for lab {hld_file}"
        assert response.data["name"] == payload["name"], "Lab not in the returning payload"
        assert (
            len(Lab.objects.filter(name=payload["name"])) == 1
        ), "Lab has not been created"
