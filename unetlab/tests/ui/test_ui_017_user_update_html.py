"""Test HTML (UI) user update."""

import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse


@pytest.mark.django_db
def test_ui_user_update_html_admin(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) user update by admin."""
    user = user_set_group_multiple["admin1"]
    client.force_login(user)
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile update tested in profile tests
            continue
        url = reverse("user_update", kwargs={"pk": u.id})
        payload = {"username": u.username, "first_name": f"First {u.username} Name"}
        response = client.post(url, payload, format="json")
        # Verify the response
        assert (
            response.status_code == 302
        ), f"Expected 302 (redirect to detail) for user {user.username}"
        # Verify the database
        target_user = User.objects.get(username=u.username)
        assert (
            target_user.first_name == payload["first_name"]
        ), f"User {u.username} has not been updated by {user.username}"


@pytest.mark.django_db
def test_ui_user_update_html_staff(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) user update by staffs."""
    user = user_set_group_multiple["staff1"]
    client.force_login(user)
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile update tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list("id", flat=True)
            & u.groups.values_list("id", flat=True)
        )
        url = reverse("user_update", kwargs={"pk": u.id})
        payload = {"username": u.username, "first_name": f"First {u.username} Name"}
        response = client.post(url, payload, format="json")
        if shared_groups and (u.is_superuser or u.is_staff):
            # Verify the response
            assert response.status_code == 403, f"Expected 403 for user {user.username}"
            # Verify the database
            target_user = User.objects.get(username=u.username)
            assert (
                target_user.first_name != payload["first_name"]
            ), f"User {u.username} must not be updated by {user.username}"
        elif shared_groups:
            # Verify the response
            assert (
                response.status_code == 302
            ), f"Expected 302 (redirect to detail) for user {user.username}"
            # Verify the database
            target_user = User.objects.get(username=u.username)
            assert (
                target_user.first_name == payload["first_name"]
            ), f"User {u.username} has not been updated by {user.username}"
        else:
            # Verify the response
            assert (
                response.status_code == 404
            ), f"User {u.username} must not be updated by {user.username}"
            # Verify the database
            target_user = User.objects.get(username=u.username)
            assert (
                target_user.first_name != payload["first_name"]
            ), f"User {u.username} must not be updated by {user.username}"


@pytest.mark.django_db
def test_ui_user_update_html_user(
    client,
    user_set_group1,
    user_set_group_multiple,
    user_set_ungrouped,
    user_set_single,
):
    """Test HTML (UI) user update by users."""
    user = user_set_group_multiple["user1"]
    client.force_login(user)
    for u in User.objects.all():
        if u.id == user.id:
            # Own profile update tested in profile tests
            continue
        shared_groups = bool(
            user.groups.values_list("id", flat=True)
            & u.groups.values_list("id", flat=True)
        )
        url = reverse("user_update", kwargs={"pk": u.id})
        payload = {"username": u.username, "first_name": f"First {u.username} Name"}
        response = client.post(url, payload, format="json")
        if shared_groups:
            assert response.status_code == 403, f"Expected 403 for user {user.username}"
            # Verify the database
            target_user = User.objects.get(username=u.username)
            assert (
                target_user.first_name != payload["first_name"]
            ), f"User {u.username} must not be updated by {user.username}"
        else:
            assert (
                response.status_code == 404
            ), f"User {u.username} must not be deleted by {user.username}"
            # Verify the database
            target_user = User.objects.get(username=u.username)
            assert (
                target_user.first_name != payload["first_name"]
            ), f"User {u.username} must not be updated by {user.username}"


@pytest.mark.django_db
def test_ui_user_update_html_guest(client, user_set_group1):
    """Test HTML (UI) user update by guest user."""
    for u in User.objects.all():
        url = reverse("user_update", kwargs={"pk": u.id})
        payload = {"username": u.username, "first_name": f"First {u.username} Name"}
        response = client.post(url, payload, format="json")
        assert response.status_code == 302, "Expected 302 (redirect to list page)"


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_user_update_html_role(client, user_set_group1, role):
    """Test DRF (API) role upgrade."""
    user = user_set_group1[role]
    client.force_login(user)
    for u in User.objects.exclude(is_superuser=True):
        payload = {"username": u.username, "is_superuser": True, "is_staff": True}
        url = reverse("user_update", kwargs={"pk": u.id})
        client.post(url, payload, format="json")
        u.refresh_from_db()
        if role == "admin" and not u.is_superuser:
            # Admins can upgrade staff/users
            assert u.is_superuser, f"Failed upgrading {u.username} by {user.username}"
        if role in ("staff", "user"):
            # Staff/users cannot upgrade anyone
            assert (
                not u.is_superuser
            ), f"User {u.username} cannot be upgraded by {user.username}"


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "staff", "user"])
def test_ui_user_update_html_groups(client, user_set_group1, role):
    """Test HTML (UI) groups change."""
    new_group, _ = Group.objects.get_or_create(name="group_new")
    user = user_set_group1[role]
    client.force_login(user)
    for u in User.objects.all():
        group_ids = set(u.groups.all().values_list("id", flat=True))
        payload = {
            "username": u.username,
            "is_active": True,
            "groups": list(group_ids) + [new_group.id],
            "is_superuser": u.is_superuser,
            "is_staff": u.is_staff,
        }
        url = reverse("user_update", kwargs={"pk": u.id})
        client.post(url, payload, format="json")
        v = User.objects.get(id=u.id)
        new_group_ids = set(v.groups.all().values_list("id", flat=True))
        if role == "admin" and not u.is_superuser:
            # Admins can upgrade users
            v = User.objects.get(id=u.id)
            assert (
                set(payload["groups"]) == new_group_ids
            ), f"Failed upgrading {u.username} by {user.username}"
        if role in ("staff", "user"):
            # Staff cannot upgrade users
            assert (
                group_ids == new_group_ids
            ), f"User {u.username} cannot be upgraded by {user.username}"
