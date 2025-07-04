"""
Pytest fixtures for testing the Job app API and models.

This module provides reusable test fixtures for setting up API clients,
user instances with different permissions, and pre-populated Job and Log
objects used across multiple test cases.

Fixtures:
- api_client: Returns a DRF APIClient instance for making HTTP requests.
- admin_user: Creates and returns a Django superuser with admin privileges.
- staff_user: Creates and returns a Django superuser with staff privileges.
- user: Creates and returns a regular Django user without special privileges.
- jobs: Creates Job and Log instances associated with each user type.
"""

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from job.models import Job, Log, LogSeverityChoices, LogTypeChoices, JobStatusChoices


@pytest.fixture
def api_client():
    """
    Provide a DRF APIClient instance for test requests.

    Returns:
        APIClient: A fresh API client instance.
    """
    return APIClient()


@pytest.fixture
def admin_user(db):
    """
    Create a superuser with admin privileges.

    Args:
        db: Django database fixture to enable DB access.

    Returns:
        User: The created admin user instance.
    """
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin_pass",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def staff_user(db):
    """
    Create a superuser with staff privileges but non-admin.

    Args:
        db: Django database fixture to enable DB access.

    Returns:
        User: The created staff user instance.
    """
    return User.objects.create_superuser(
        username="staff",
        email="staff@example.com",
        password="staff_pass",
        is_staff=True,
    )


@pytest.fixture
def user(db):
    """
    Create a regular Django user without special permissions.

    Args:
        db: Django database fixture to enable DB access.

    Returns:
        User: The created regular user instance.
    """
    return User.objects.create_user(
        username="user", email="user@example.com", password="user_pass"
    )


@pytest.fixture
def jobs(admin_user, staff_user, user):
    """
    Create Job and associated Log instances for each user type.

    Args:
        db: Django database fixture.
        admin_user: Admin user fixture.
        staff_user: Staff user fixture.
        user: Regular user fixture.

    Returns:
        dict: Dictionary with keys 'admin', 'staff', 'user' containing the corresponding Job instances.
    """
    admin_job = Job.objects.create(user=admin_user.username)
    Log.objects.create(
        job=admin_job,
        message="Admin log message",
        severity=LogSeverityChoices.ERROR,
        source="testhost",
        type=LogTypeChoices.APP,
    )
    staff_job = Job.objects.create(
        user=staff_user.username, status=JobStatusChoices.SUCCEEDED
    )
    Log.objects.create(
        job=staff_job,
        message="Staff log message",
        severity=LogSeverityChoices.ERROR,
        source="testhost",
        type=LogTypeChoices.APP,
    )
    user_job = Job.objects.create(user=user.username)
    Log.objects.create(
        job=user_job,
        message="User log message",
        severity=LogSeverityChoices.ERROR,
        source="testhost",
        type=LogTypeChoices.APP,
    )
    other_job = Job.objects.create(user="other")
    Log.objects.create(
        job=other_job,
        message="Other log message",
        severity=LogSeverityChoices.ERROR,
        source="testhost",
        type=LogTypeChoices.APP,
    )
    return {
        "admin": admin_job,
        "staff": staff_job,
        "user": user_job,
        "other": other_job,
    }
