# TODO
# import pytest
# from job.models import Job, Log, LogSeverityChoices, LogTypeChoices
# from job.serializers import JobSerializer, LogSerializer

# @pytest.mark.django_db
# def test_job_serializer():
#     job = Job.objects.create(user="andrea")
#     serializer = JobSerializer(job)
#     data = serializer.data
#     assert data['user'] == "andrea"
#     assert 'id' in data

# @pytest.mark.django_db
# def test_log_serializer():
#     job = Job.objects.create(user="andrea")
#     log = Log.objects.create(
#         job=job,
#         message="msg",
#         severity=LogSeverityChoices.INFO,
#         source="source",
#         type=LogTypeChoices.APP,
#     )
#     serializer = LogSerializer(log)
#     data = serializer.data
#     assert data['message'] == "msg"
#     assert data['job'] == job.pk
