# tests/test_permissions.py
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from myapp.models import Job, Log
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username='normal', password='test123')

@pytest.fixture
def staff():
    return User.objects.create_user(username='admin', password='test123', is_staff=True)

@pytest.fixture
def job(user):
    return Job.objects.create(user=user, status="PENDING")

@pytest.mark.django_db
def test_normal_user_can_see_own_job(user, job):
    client = APIClient()
    client.force_authenticate(user=user)
    res = client.get(f'/jobs/{job.id}/')
    assert res.status_code == 200

@pytest.mark.django_db
def test_normal_user_cannot_see_others_job(staff, user, job):
    job.user = staff
    job.save()
    client = APIClient()
    client.force_authenticate(user=user)
    res = client.get(f'/jobs/{job.id}/')
    assert res.status_code == 403

@pytest.mark.django_db
def test_staff_can_see_all_jobs(staff, job):
    client = APIClient()
    client.force_authenticate(user=staff)
    res = client.get(f'/jobs/{job.id}/')
    assert res.status_code == 200