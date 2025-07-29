import pytest
from job.models import JobStatusChoices
from job.filters import JobFilter
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
def test_job_filters_user(jobs):
    """
    Test filtering Jobs by user using the pre-created jobs fixture.
    """
    qs = JobFilter(data={"username": "user"}).qs
    assert list(qs) == [jobs["user"]]


@pytest.mark.django_db
def test_job_filters_status(jobs):
    """
    Test filtering Jobs by user using the pre-created jobs fixture.
    """
    qs_created = JobFilter(data={"status": JobStatusChoices.CREATED}).qs
    assert len(qs_created) == 3, "Expected 3 jobs with status 'CREATED'."
    qs_succeeded = JobFilter(data={"status": JobStatusChoices.SUCCEEDED}).qs
    assert len(qs_succeeded) == 1, "Expected 1 job with status 'SUCCEEDED'."


# TODO Log
# @pytest.mark.django_db
# def test_log_filter_by_severity():
#     job = Job.objects.create(user="andrea")
#     Log.objects.create(
#         job=job,
#         message="error",
#         severity=LogSeverityChoices.ERROR,
#         source="src",
#         type=LogTypeChoices.APP,
#     )
#     Log.objects.create(
#         job=job,
#         message="info",
#         severity=LogSeverityChoices.INFO,
#         source="src",
#         type=LogTypeChoices.APP,
#     )
#     filtered = LogFilter({"severity": LogSeverityChoices.ERROR}, queryset=Log.objects.all())
#     assert filtered.qs.count() == 1
