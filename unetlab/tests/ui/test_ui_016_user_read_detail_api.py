"""Test DRF (API) user view."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_user_read_detail_api_admin(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user detail view by admin."""
    for user in User.objects.filter(is_superuser=True):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token}"}
        for u in User.objects.all():
            url = reverse("user-detail", kwargs={"pk": u.id})
            response = api_client.get(url, headers=headers)
            assert (
                response.status_code == 200
            ), f"User {u.username} not found by {user.username}"


@pytest.mark.django_db
def test_ui_user_read_detail_api_user(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user detail view by staffs and users."""
    for user in User.objects.filter(is_superuser=False):
        token, _ = Token.objects.get_or_create(user=user)
        headers = {"Authorization": f"Token {token}"}
        all_users = User.objects.all()
        # Testing users with a shared group
        all_users_w_shared_group = all_users.filter(groups__in=user.groups.all())
        for u in all_users_w_shared_group:
            url = reverse("user-detail", kwargs={"pk": u.id})
            response = api_client.get(url, headers=headers)
            assert (
                response.status_code == 200
            ), f"User {u.username} not found by {user.username}"
        # Testing users without a shared group
        all_users_wo_shared_group = all_users.exclude(
            username__in=list(
                all_users_w_shared_group.values_list("username", flat=True)
            )
            + [user.username]
        )
        for u in all_users_wo_shared_group:
            url = reverse("user-detail", kwargs={"pk": u.id})
            response = api_client.get(url, headers=headers)
            assert response.status_code == 404, f"User {user.username} must not see {u}"


@pytest.mark.django_db
def test_ui_user_read_detail_api_guest(api_client, user_set_group1):
    """Test DRS (API) user detail view by guest user."""
    for u in User.objects.all():
        url = reverse("user-detail", kwargs={"pk": u.id})
        response = api_client.get(url)
        assert response.status_code == 401, "Expected 401 for guest user"
