"""Testing permissions in Job app."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_job_permissions_ui_joblist_admin(client, admin_user, jobs):
    """Test Job access via UI with admin user."""
    client.login(username='admin', password='admin_pass')
    url = reverse('job_list')
    response = client.get(url)
    assert response.status_code == 200, 'Admin job list UI did not return 200 OK'
    assert b'<td>admin</td>' in response.content, 'Admin job not found in job list UI'
    assert b'<td>staff</td>' in response.content, 'Staff job not found in job list UI'
    assert b'<td>user</td>' in response.content, 'User job not found in job list UI'
    assert b'<td>other</td>' in response.content, 'Other job not found in job list UI'


@pytest.mark.django_db
def test_job_permissions_ui_joblist_staff(client, staff_user, jobs):
    """Test Job access via UI with staff user."""
    client.login(username='staff', password='staff_pass')
    url = reverse('job_list')
    response = client.get(url)
    assert response.status_code == 200, 'Staff job list UI did not return 200 OK'
    assert b'<td>admin</td>' in response.content, 'Admin job not found in job list UI'
    assert b'<td>staff</td>' in response.content, 'Staff job not found in job list UI'
    assert b'<td>user</td>' in response.content, 'User job not found in job list UI'
    assert b'<td>other</td>' in response.content, 'Other job not found in job list UI'


@pytest.mark.django_db
def test_job_permissions_ui_joblist_user(client, user, jobs):
    """Test Job access via UI with unprivileged user."""
    client.login(username='user', password='user_pass')
    url = reverse('job_list')
    response = client.get(url)
    assert response.status_code == 200, 'User job list UI did not return 200 OK'
    assert b'<td>admin</td>' not in response.content, (
        'Admin job should not be visible to user'
    )
    assert b'<td>staff</td>' not in response.content, (
        'Staff job should not be visible to user'
    )
    assert b'<td>user</td>' in response.content, 'User job should be visible to user'
    assert b'<td>other</td>' not in response.content, (
        'Other job should not be visible to user'
    )


@pytest.mark.django_db
def test_job_permissions_ui_joblist_guest(client):
    """Test Job access via UI with non-existent user."""
    client.login(username='guest', password='guest_pass')
    url = reverse('job_list')
    response = client.get(url)
    assert response.status_code == 302, (
        'Guest user should be redirected (302) when accessing job list UI'
    )


@pytest.mark.django_db
def test_job_permissions_ui_jobdetail_admin(client, admin_user, jobs):
    """Test Job detail access via UI with admin user."""
    client.login(username='admin', password='admin_pass')

    for key in ['admin', 'staff', 'user', 'other']:
        url = reverse('job_detail', args=[jobs[key].pk])
        response = client.get(url)
        assert response.status_code == 200, (
            f'Admin user cannot access job detail for {key} job'
        )


@pytest.mark.django_db
def test_job_permissions_ui_jobdetail_staff(client, staff_user, jobs):
    """Test Job detail access via UI with staff user."""
    client.login(username='staff', password='staff_pass')

    for key in ['admin', 'staff', 'user', 'other']:
        url = reverse('job_detail', args=[jobs[key].pk])
        response = client.get(url)
        assert response.status_code == 200, (
            f'Staff user cannot access job detail for {key} job'
        )


@pytest.mark.django_db
def test_job_permissions_ui_jobdetail_user(client, user, jobs):
    """Test Job detail access via UI with unprivileged user."""
    client.login(username='user', password='user_pass')

    for key in ['admin', 'staff', 'other']:
        url = reverse('job_detail', args=[jobs[key].pk])
        response = client.get(url)
        assert response.status_code == 403, f'User should get 403 for {key} job detail'

    url = reverse('job_detail', args=[jobs['user'].pk])
    response = client.get(url)
    assert response.status_code == 200, 'User cannot access own job detail'


@pytest.mark.django_db
def test_job_permissions_ui_jobdetail_guest(client, jobs):
    """Test Job detail access via UI with non-existent user."""
    client.login(username='guest', password='guest_pass')
    url = reverse('job_detail', args=[jobs['other'].pk])
    response = client.get(url)
    assert response.status_code == 302, (
        'Guest user should be redirected (302) when accessing job detail UI'
    )
