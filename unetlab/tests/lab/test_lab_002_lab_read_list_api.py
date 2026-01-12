"""Test DRF (API) lab list."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.authtoken.models import Token
from lab.models import Lab


@pytest.mark.django_db
def test_lab_group_read_list_api_admin(
    api_client,
    user_set_group1,
    user_set_ungrouped,
):
    """Test DRF (API) lab list view by admin."""
    for user in User.objects.filter(is_superuser=True):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token}"}
        all_labs = Lab.objects.all().values_list("id", flat=True)
        url = reverse("lab-list") + f"?per_page={len(all_labs)}"
        response = api_client.get(url, headers=headers)
        assert response.status_code == 200, f"Failed for user {user.username}"
        result_labs = [l["id"] for l in response.data["results"]]
        # for g in all_groups:
        #     assert g in result_groups, f"Group {g} not found by {user.username}"


# @pytest.mark.django_db
# def test_ui_group_read_list_api_user(
#     api_client,
#     user_set_group1,
#     user_set_group_multiple,
#     user_set_ungrouped,
#     user_set_single,
# ):
#     """Test DRF (API) user list view by staffs and users."""
#     for user in User.objects.filter(is_superuser=False):
#         token, _ = Token.objects.get_or_create(user=user)
#         headers = {"Authorization": f"Token {token}"}
#         all_groups = Group.objects.all()
#         url = reverse("group-list") + f"?per_page={len(all_groups)}"
#         response = api_client.get(url, headers=headers)
#         assert response.status_code == 200, f"Failed for user {user.username}"
#         result_groups = [g["name"] for g in response.data["results"]]
#         # Testing user groups
#         user_groups = user.groups.all().values_list("name", flat=True)
#         for g in user_groups:
#             assert g in result_groups, f"Group {g} not found by {user.username}"
#         # Testing other groups
#         other_groups = Group.objects.exclude(name__in=user_groups).values_list(
#             "name", flat=True
#         )
#         for g in other_groups:
#             assert g not in result_groups, f"User {user.username} must not see {g}"


# @pytest.mark.django_db
# def test_ui_group_read_list_api_guest(api_client):
#     """Test DRS (API) group list view by guest user."""
#     url = reverse("group-list")
#     response = api_client.get(url)
#     assert response.status_code == 401, "Expected 401 for guest user"
