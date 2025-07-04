# import pytest
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User
# from job.models import Job, Log, LogSeverityChoices, LogTypeChoices

# @pytest.mark.django_db
# def test_job_api_list_authenticated_user():
#     user = User.objects.create_user(username="andrea", password="test")
#     Job.objects.create(user="andrea")
#     client = APIClient()
#     client.force_authenticate(user=user)
#     response = client.get("/api/job/")
#     assert response.status_code == 200
#     assert len(response.data) == 1

# @pytest.mark.django_db
# def test_job_api_forbidden_other_user():
#     user = User.objects.create_user(username="andrea", password="test")
#     Job.objects.create(user="mario")
#     client = APIClient()
#     client.force_authenticate(user=user)
#     response = client.get("/api/job/")
#     assert response.status_code == 200
#     assert len(response.data) == 0

# @pytest.mark.django_db
# def test_log_api_filter_by_severity():
#     user = User.objects.create_user(username="andrea", password="test")
#     job = Job.objects.create(user="andrea")
#     Log.objects.create(
#         job=job,
#         message="Test log",
#         severity=LogSeverityChoices.ERROR,
#         source="source",
#         type=LogTypeChoices.APP,
#     )
#     client = APIClient()
#     client.force_authenticate(user=user)
#     response = client.get(f"/api/log/?severity={LogSeverityChoices.ERROR}")
#     assert response.status_code == 200
#     assert len(response.data) == 1
