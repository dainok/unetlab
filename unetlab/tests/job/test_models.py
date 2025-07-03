import pytest
from job.models import Job, Log, JobStatusChoices, LogSeverityChoices, LogTypeChoices

@pytest.mark.django_db
def test_create_job():
    """Test Job creation."""
    job = Job.objects.create(
        user="admin",
    )
    assert str(job) == str(job.pk)
    assert job.status == JobStatusChoices.CREATED.value
    assert job.user == "admin"


@pytest.mark.django_db
def test_create_log():
    """Test Job and Log creation."""
    job = Job.objects.create(
        user="admin",
    )
    assert str(job) == str(job.pk)
    assert job.status == JobStatusChoices.CREATED.value
    assert job.user == "admin"

    log = Log.objects.create(
        job=job,
        message="Test message",
        severity=LogSeverityChoices.ERROR,
        source="testhost",
        type=LogTypeChoices.APP,
    )

    assert str(log) == str(log.pk)
    assert not log.acknowledged
    assert log.job == job
    assert log.message == "Test message"
    assert log.severity == LogSeverityChoices.ERROR
    assert log.source == "testhost"
    assert log.type == "APP"
