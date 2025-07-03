"""Testing permissions in Job app."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_job_permissions_ui_joblist_admin(client, admin_user, jobs):
    """Test Job access via UI with admin user."""
    client.login(username="admin", password="admin_pass")
    url = reverse("job_list")
    response = client.get(url)
    assert response.status_code == 200
    assert b"<td>admin</td>" in response.content
    assert b"<td>staff</td>" in response.content
    assert b"<td>user</td>" in response.content
    assert b"<td>other</td>" in response.content


@pytest.mark.django_db
def test_job_permissions_ui_joblist_staff(client, staff_user, jobs):
    """Test Job access via UI with staff user."""
    client.login(username="staff", password="staff_pass")
    url = reverse("job_list")
    response = client.get(url)
    assert response.status_code == 200
    assert b"<td>admin</td>" in response.content
    assert b"<td>staff</td>" in response.content
    assert b"<td>user</td>" in response.content
    assert b"<td>other</td>" in response.content


@pytest.mark.django_db
def test_job_permissions_ui_joblist_user(client, user, jobs):
    """Test Job access via UI with unprivileged user."""
    client.login(username="user", password="user_pass")
    url = reverse("job_list")
    response = client.get(url)
    assert response.status_code == 200
    assert b"<td>admin</td>" not in response.content
    assert b"<td>staff</td>" not in response.content
    assert b"<td>user</td>" in response.content
    assert b"<td>other</td>" not in response.content


@pytest.mark.django_db
def test_job_permissions_ui_jobdetail_admin(client, admin_user, jobs):
    """Test Job detail access via UI with admin user."""
    client.login(username="admin", password="admin_pass")
    url = reverse("job_detail", args=[jobs["admin"].pk])
    response = client.get(url)
    assert response.status_code == 200
    url = reverse("job_detail", args=[jobs["staff"].pk])
    response = client.get(url)
    assert response.status_code == 200
    url = reverse("job_detail", args=[jobs["user"].pk])
    response = client.get(url)
    assert response.status_code == 200
    url = reverse("job_detail", args=[jobs["other"].pk])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_job_permissions_ui_jobdetail_staff(client, staff_user, jobs):
    """Test Job detail access via UI with staff user."""
    client.login(username="staff", password="admin_pass")
    url = reverse("job_detail", args=[jobs["admin"].pk])
    response = client.get(url)
    assert response.status_code == 200
    url = reverse("job_detail", args=[jobs["staff"].pk])
    response = client.get(url)
    assert response.status_code == 200
    url = reverse("job_detail", args=[jobs["user"].pk])
    response = client.get(url)
    assert response.status_code == 200
    url = reverse("job_detail", args=[jobs["other"].pk])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_job_permissions_ui_jobdetail_user(client, user, jobs):
    """Test Job detail access via UI with staff user."""
    client.login(username="user", password="admin_pass")
    url = reverse("job_detail", args=[jobs["admin"].pk])
    response = client.get(url)
    assert response.status_code == 403
    url = reverse("job_detail", args=[jobs["staff"].pk])
    response = client.get(url)
    assert response.status_code == 403
    url = reverse("job_detail", args=[jobs["user"].pk])
    response = client.get(url)
    assert response.status_code == 200
    url = reverse("job_detail", args=[jobs["other"].pk])
    response = client.get(url)
    assert response.status_code == 403
