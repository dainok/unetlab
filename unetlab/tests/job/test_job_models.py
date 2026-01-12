"""Tests for Job and Log models with detailed documentation."""

import pytest
from job.models import Job, Log, JobStatusChoices, LogSeverityChoices, LogTypeChoices


@pytest.mark.django_db
def test_job_models_job_create():
    """
    Test the creation of a Job instance.

    Verifies that:
    - A Job object is created with the specified user.
    - The string representation returns the primary key as a string.
    - The default status is set to 'CREATED'.
    """
    job = Job.objects.create(username='admin')

    # Check that __str__ returns the primary key as string
    assert str(job) == str(job.pk), 'Job __str__ should return primary key as string'

    # Check that the default status is CREATED
    assert job.status == JobStatusChoices.CREATED.value, (
        'Default job status should be CREATED'
    )

    # Check that the user is set correctly
    assert job.username == 'admin', 'Job user should match the provided value'


@pytest.mark.django_db
def test_job_models_log_create():
    """
    Test the creation of a Log instance related to a Job.

    Verifies that:
    - A Job object can be created.
    - A Log object linked to the Job can be created with proper attributes.
    - The string representation of Log returns the primary key as string.
    - Default acknowledged field is False.
    - All provided fields (severity, source, type) are set correctly.
    """
    job = Job.objects.create(username='admin')

    # Verify Job creation
    assert str(job) == str(job.pk), 'Job __str__ should return primary key as string'
    assert job.status == JobStatusChoices.CREATED.value, (
        'Default job status should be CREATED'
    )
    assert job.username == 'admin', 'Job user should match the provided value'

    # Create a Log entry associated with the Job
    log = Log.objects.create(
        job=job,
        message='Test message',
        severity=LogSeverityChoices.ERROR,
        source='testhost',
        type=LogTypeChoices.APP,
    )

    # Check string representation returns primary key
    assert str(log) == str(log.pk), 'Log __str__ should return primary key as string'

    # Confirm default acknowledged value is False
    assert not log.acknowledged, 'Default acknowledged field should be False'

    # Validate all assigned fields
    assert log.job == job, 'Log.job should reference the associated Job'
    assert log.message == 'Test message', 'Log message should be set correctly'
    assert log.severity == LogSeverityChoices.ERROR, (
        'Log severity should match assigned value'
    )
    assert log.source == 'testhost', 'Log source should match assigned value'
    assert log.type == LogTypeChoices.APP, 'Log type should match assigned value'
