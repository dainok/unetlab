"""Test DRF (API) user deletion."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_ui_user_delete_api_admin(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user deletion by admin."""
    user = user_set_group_multiple["admin1"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        url = reverse("user-detail", kwargs={"pk": u.id})
        response = api_client.delete(url, headers=headers)
        assert (
            response.status_code == 204
        ), f"User {u.username} not found by {user.username}"
        assert (
            len(User.objects.filter(username=u.username)) == 0
        ), f"User {u.username} has not been deleted by {user.username}"


@pytest.mark.django_db
def test_ui_user_delete_api_staff(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user deletion by staffs."""
    user = user_set_group_multiple["staff1"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list("id", flat=True)
            & u.groups.values_list("id", flat=True)
        )
        url = reverse("user-detail", kwargs={"pk": u.id})
        response = api_client.delete(url, headers=headers)
        if shared_groups and (u.is_superuser or u.is_staff):
            assert (
                response.status_code == 403
            ), f"User {u.username} must not be deleted by {user.username}"
            assert (
                len(User.objects.filter(id=u.id)) == 1
            ), f"User {u.username} has been deleted"
        elif shared_groups:
            assert (
                response.status_code == 204
            ), f"User {u.username} must be deleted by {user.username}"
            assert (
                len(User.objects.filter(id=u.id)) == 0
            ), f"User {u.username} has not been deleted"
        else:
            assert (
                response.status_code == 404
            ), f"User {u.username} must not be deleted by {user.username}"
            assert (
                len(User.objects.filter(id=u.id)) == 1
            ), f"User {u.username} has been deleted"


@pytest.mark.django_db
def test_ui_user_delete_api_user(
    api_client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test DRF (API) user deletion by users."""
    user = user_set_group_multiple["user1"]
    token, _ = Token.objects.get_or_create(user=user)
    headers = {"Authorization": f"Token {token}"}
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile deletion tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list("id", flat=True)
            & u.groups.values_list("id", flat=True)
        )
        url = reverse("user-detail", kwargs={"pk": u.id})
        response = api_client.delete(url, headers=headers)
        if shared_groups:
            assert (
                response.status_code == 403
            ), f"User {u.username} must not be deleted by {user.username}"
            assert (
                len(User.objects.filter(id=u.id)) == 1
            ), f"User {u.username} has been deleted"
        else:
            assert (
                response.status_code == 404
            ), f"User {u.username} must not be deleted by {user.username}"
            assert (
                len(User.objects.filter(id=u.id)) == 1
            ), f"User {u.username} has been deleted"


@pytest.mark.django_db
def test_ui_user_delete_api_guest(api_client, user_set_group1):
    """Test DRS (API) user deletion by guest user."""
    for u in User.objects.all():
        url = reverse("user-detail", kwargs={"pk": u.id})
        response = api_client.delete(url)
        assert response.status_code == 401, "Expected 401 for guest user"
