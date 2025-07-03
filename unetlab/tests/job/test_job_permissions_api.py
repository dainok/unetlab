"""Testing permissions in Job app."""


def test_job_permissions_api_joblist_admin(api_client, admin_user, jobs):
    """Test Job access via API with admin user."""
    api_client.force_authenticate(user=admin_user)
    response = api_client.get("/api/job/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert isinstance(response.data["results"], list)
    assert len(response.data["results"]) == 4


def test_job_permissions_api_joblist_staff(api_client, staff_user, jobs):
    """Test Job access via API with staff user."""
    api_client.force_authenticate(user=staff_user)
    response = api_client.get("/api/job/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert isinstance(response.data["results"], list)
    assert len(response.data["results"]) == 4


def test_job_permissions_api_joblist_user(api_client, user, jobs):
    """Test Job access via API with unprivileged user."""
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/job/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert isinstance(response.data["results"], list)
    assert len(response.data["results"]) == 1


def test_job_permissions_api_joblist_guest(api_client, db):
    """Test Job access via API with non-existent user."""
    response = api_client.get("/api/job/")
    assert response.status_code == 401


def test_job_permissions_api_jobdetail_admin(api_client, admin_user, jobs):
    """Test Job access via API with admin user."""
    api_client.force_authenticate(user=admin_user)
    response = api_client.get(f"/api/job/{jobs['admin'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "admin"
    response = api_client.get(f"/api/job/{jobs['staff'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "staff"
    response = api_client.get(f"/api/job/{jobs['user'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "user"
    response = api_client.get(f"/api/job/{jobs['other'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "other"


def test_job_permissions_api_jobdetail_staff(api_client, staff_user, jobs):
    """Test Job access via API with admin user."""
    api_client.force_authenticate(user=staff_user)
    response = api_client.get(f"/api/job/{jobs['admin'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "admin"
    response = api_client.get(f"/api/job/{jobs['staff'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "staff"
    response = api_client.get(f"/api/job/{jobs['user'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "user"
    response = api_client.get(f"/api/job/{jobs['other'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "other"


def test_job_permissions_api_jobdetail_user(api_client, user, jobs):
    """Test Job access via API with admin user."""
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/job/{jobs['admin'].pk}/")
    assert response.status_code == 404
    response = api_client.get(f"/api/job/{jobs['staff'].pk}/")
    assert response.status_code == 404
    response = api_client.get(f"/api/job/{jobs['user'].pk}/")
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.json()["status"] == "CREATED"
    assert response.json()["user"] == "user"
    response = api_client.get(f"/api/job/{jobs['other'].pk}/")
    assert response.status_code == 404


def test_job_permissions_api_jobdetail_guest(api_client, jobs):
    """Test Job access via API with admin user."""
    api_client.force_authenticate(user=None)
    response = api_client.get(f"/api/job/{jobs['admin'].pk}/")
    assert response.status_code == 401
    response = api_client.get(f"/api/job/{jobs['staff'].pk}/")
    assert response.status_code == 401
    response = api_client.get(f"/api/job/{jobs['user'].pk}/")
    assert response.status_code == 401
    response = api_client.get(f"/api/job/{jobs['other'].pk}/")
    assert response.status_code == 401
