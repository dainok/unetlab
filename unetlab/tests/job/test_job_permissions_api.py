"""
Tests for Job API permissions.

These tests verify that the API endpoints for listing and retrieving Job instances
correctly enforce permission rules based on user roles:
- Admin and Staff users can see all jobs.
- Normal users can only see their own jobs.
- Unauthenticated users are denied access.

Fixtures required:
- api_client: a Django REST Framework test client.
- admin_user, staff_user, user: User instances with different roles.
- jobs: a dictionary of Job instances keyed by user role ('admin', 'staff', 'user', 'other').
"""

import pytest


@pytest.mark.django_db
def test_job_permissions_api_joblist_admin(api_client, admin_user, jobs):
    """Admin users can see all jobs."""
    api_client.force_authenticate(user=admin_user)
    response = api_client.get("/api/job/")
    assert response.status_code == 200, "Admin job list API did not return 200 OK"
    assert isinstance(response.data, dict), "Response data is not a dict (pagination)"
    assert isinstance(response.data["results"], list), "'results' is not a list"
    assert len(response.data["results"]) == 4, "Admin user should see 4 jobs"


@pytest.mark.django_db
def test_job_permissions_api_joblist_staff(api_client, staff_user, jobs):
    """Staff users can see all jobs."""
    api_client.force_authenticate(user=staff_user)
    response = api_client.get("/api/job/")
    assert response.status_code == 200, "Staff job list API did not return 200 OK"
    assert isinstance(response.data, dict), "Response data is not a dict (pagination)"
    assert isinstance(response.data["results"], list), "'results' is not a list"
    assert len(response.data["results"]) == 4, "Staff user should see 4 jobs"


@pytest.mark.django_db
def test_job_permissions_api_joblist_user(api_client, user, jobs):
    """Normal users can only see their own jobs."""
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/job/")
    assert response.status_code == 200, "User job list API did not return 200 OK"
    assert isinstance(response.data, dict), "Response data is not a dict (pagination)"
    assert isinstance(response.data["results"], list), "'results' is not a list"
    assert len(response.data["results"]) == 1, "User should see only their own job"


@pytest.mark.django_db
def test_job_permissions_api_joblist_guest(api_client, db):
    """Unauthenticated users cannot access job list."""
    response = api_client.get("/api/job/")
    assert (
        response.status_code == 401
    ), "Guest job list API should return 401 Unauthorized"


@pytest.mark.django_db
def test_job_permissions_api_jobdetail_admin(api_client, admin_user, jobs):
    """Admin can see all job details."""
    api_client.force_authenticate(user=admin_user)
    for key, job in jobs.items():
        response = api_client.get(f"/api/job/{job.pk}/")
        assert (
            response.status_code == 200
        ), f"Admin could not access job detail for job {job.pk}"
        assert isinstance(response.data, dict), "Response data is not a dict"
        assert response.data["status"] in [
            "CREATED",
            "SUCCEEDED",
        ], "Job status is neither 'CREATED' nor 'SUCCEEDED'"
        assert response.data["username"] == job.username, "Job user does not match"


@pytest.mark.django_db
def test_job_permissions_api_jobdetail_staff(api_client, staff_user, jobs):
    """Staff can see all job details."""
    api_client.force_authenticate(user=staff_user)
    for key, job in jobs.items():
        response = api_client.get(f"/api/job/{job.pk}/")
        assert (
            response.status_code == 200
        ), f"Staff could not access job detail for job {job.pk}"
        assert isinstance(response.data, dict), "Response data is not a dict"
        assert response.data["status"] in [
            "CREATED",
            "SUCCEEDED",
        ], "Job status is neither 'CREATED' nor 'SUCCEEDED'"
        assert response.data["username"] == job.username, "Job user does not match"


@pytest.mark.django_db
def test_job_permissions_api_jobdetail_user(api_client, user, jobs):
    """Users can only see their own job details; others return 404."""
    api_client.force_authenticate(user=user)

    for key in ["admin", "staff", "other"]:
        response = api_client.get(f"/api/job/{jobs[key].pk}/")
        assert (
            response.status_code == 404
        ), f"User accessed job {jobs[key].pk} they should not see"

    response = api_client.get(f"/api/job/{jobs['user'].pk}/")
    assert response.status_code == 200, "User could not access own job detail"
    assert isinstance(response.data, dict), "Response data is not a dict"
    assert response.data["status"] == "CREATED", "Job status is not 'CREATED'"
    assert response.data["username"] == jobs["user"].username, "Job user does not match"


@pytest.mark.django_db
def test_job_permissions_api_jobdetail_guest(api_client, jobs):
    """Unauthenticated users cannot access job details."""
    api_client.force_authenticate(user=None)
    for key, job in jobs.items():
        response = api_client.get(f"/api/job/{job.pk}/")
        assert (
            response.status_code == 401
        ), f"Guest accessed job detail {job.pk} without authentication"


# TODO: LOG
