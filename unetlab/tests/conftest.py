"""
Pytest fixtures for testing UNetLab via DRF (API) and CBV.
"""

from pathlib import Path
import pytest
from django.contrib.auth.models import Group, User
from django.template.defaultfilters import slugify
from rest_framework.test import APIClient
from lab.models import Lab


# ==============================================================================
# Helpers
# ==============================================================================


@pytest.fixture
def api_client():
    """Provide a DRF APIClient instance for test requests."""
    return APIClient()


@pytest.fixture
def create_user(db):  # pylint: disable=unused-argument
    """Provide fixture to create users and groups."""

    def make_user(username, role='user', groups=None):
        """Create user given username, role and a list of groups."""
        if groups is None:
            groups = []
        if isinstance(groups, str):
            groups = [groups]

        email = f'{username}@example.com'
        password = f'{username}123'

        if role == 'admin':
            # Create an admin user
            user = User.objects.create_superuser(
                email=email,
                password=password,
                username=username,
            )
        else:
            # Create a staff o standard user
            is_staff = False
            if role == 'staff':
                is_staff = True
            user = User.objects.create_user(
                email=email,
                is_staff=is_staff,
                password=password,
                username=username,
            )

        for group in groups:
            # Create each group and add the user to it
            group, _ = Group.objects.get_or_create(name=group)
            user.groups.add(group)

        return user

    return make_user


@pytest.fixture
def create_lab(db):  # pylint: disable=unused-argument
    """Provide fixture to create users and groups."""

    def make_labs(user):
        """Create a lab associated to a username."""
        # Load HLD from file
        hld_dir = Path(__file__).parent / 'hld'
        hld_files = sorted(hld_dir.glob('hld-*.yml'))
        for hld_file in hld_files:
            with open(hld_file, encoding='utf-8') as fh:
                hld = fh.read()

            # Create the lab
            Lab.objects.create(
                name=f'Lab from {slugify(hld_file)} file',
                user=user,
                hld=hld,
            )

            # Create the shared lab
            groups = user.groups.all()
            if groups:
                Lab.objects.create(
                    name=f'Shared lab from {slugify(hld_file)} file',
                    user=user,
                    hld=hld,
                    shared_group=groups.first(),
                )

    return make_labs


# ==============================================================================
# Users and Groups
# ==============================================================================


@pytest.fixture
def _user_set_group1(db, create_user, create_lab):  # pylint: disable=unused-argument,redefined-outer-name
    """Create admin, staff and standard user within the same group."""
    users = {
        'admin': create_user('admin11', role='admin', groups='group1'),
        'staff': create_user('staff11', role='staff', groups='group1'),
        'user': create_user('user11', groups='group1'),
    }
    for user in users.values():
        create_lab(user)
    return users


@pytest.fixture
def _user_set_ungrouped(db, create_user, create_lab):  # pylint: disable=unused-argument,redefined-outer-name
    """Create admin, staff and standard user with no group."""
    users = {
        'admin': create_user('admin31', role='admin'),
        'staff': create_user('staff31', role='staff'),
        'user': create_user('user31'),
    }
    for user in users.values():
        create_lab(user)
    return users


@pytest.fixture
def _user_set_single(db, create_user, create_lab):  # pylint: disable=unused-argument,redefined-outer-name
    """Create admin, staff and standard user, each one with a dedicated group."""
    users = {
        'admin': create_user('admin41', role='admin', groups='group4'),
        'staff': create_user('staff51', role='staff', groups='group5'),
        'user': create_user('user61', groups='group6'),
    }
    for user in users.values():
        create_lab(user)
    return users
