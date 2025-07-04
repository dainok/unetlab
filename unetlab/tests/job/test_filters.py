# import pytest
# from job.models import Job, Log, LogSeverityChoices, LogTypeChoices
# from job.filters import JobFilter, LogFilter

# @pytest.mark.django_db
# def test_job_filter_user():
#     Job.objects.create(user="andrea")
#     Job.objects.create(user="mario")
#     filtered = JobFilter({"user": "andrea"}, queryset=Job.objects.all())
#     assert filtered.qs.count() == 1

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
