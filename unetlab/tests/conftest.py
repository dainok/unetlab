import pytest
from django.contrib.auth.models import User
from job.models import Job, Log, LogSeverityChoices, LogTypeChoices


@pytest.fixture
def admin_user(db):
    """Create admin user."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin_pass",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def staff_user(db):
    """Create staff user."""
    return User.objects.create_superuser(
        username="staff",
        email="staff@example.com",
        password="staff_pass",
        is_staff=True,
    )


@pytest.fixture
def user(db):
    """Create unprivileged user."""
    return User.objects.create_user(
        username="user", email="user@example.com", password="user_pass"
    )


@pytest.fixture
def jobs(admin_user, staff_user, user):
    """Create jobs and associate logs."""
    admin_job = Job.objects.create(user=admin_user.username)
    Log.objects.create(
        job=admin_job,
        message="Admin log message",
        severity=LogSeverityChoices.ERROR,
        source="testhost",
        type=LogTypeChoices.APP,
    )
    staff_job = Job.objects.create(user=staff_user.username)
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
