#!/usr/bin/env python3
""" Tasks """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import ipaddress, os, requests, sh, shutil, urllib3
from controller import celery, config
from controller.catalog.models import *
urllib3.disable_warnings()

def updateTask(task_id, username, status, message, progress):
    task = TaskTable.query.get(task_id)
    if task:
        # Update the existing task
        task.status = status
        task.message = message
        task.progress = progress
    else:
        # Add a new task
        task = TaskTable(
            id = task_id,
            status = status,
            message = message,
            progress = progress,
            username = username
        )
        db.session.add(task)
    db.session.commit()
    return {
        'status': status,
        'message': message,
        'task': task_id,
        'progress': 100,
        'username': username
    }

@celery.task(bind = True)
def addGit(self, started_by, repository_id, url, username = None, password = None):
    # Add a git repository for labs
    task_id = addGit.request.id
    self.update_state(state = 'STARTED', meta = updateTask(task_id, username = started_by, status = 'started', progress = -1,
        message = 'Starting to clone repository "{}" from "{}"'.format(repository_id, url)
    ))
    if os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository_id)):
        # Repository already exists
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Repository already "{}" exists'.format(repository_id),
            progress = 100
        )
    try:
        sh.git('-C', '{}'.format(config['app']['lab_repository']), 'clone', '-q', url, repository_id, _bg = False)
    except Exception as err:
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to clone repository "{}" from "{}" ({})'.format(repository_id, url, err),
            progress = 100
        )
    repository = RepositoryTable(
        id = repository_id,
        url = url,
        username = username,
        password = password
    )
    db.session.add(repository)
    db.session.commit()
    return updateTask(
        task_id = task_id,
        username = started_by,
        status = 'completed',
        message = 'Repository "{}" successfully cloned from "{}"'.format(repository.id, url),
        progress = 100
    )

@celery.task(bind = True)
def deleteGit(self, started_by, repository_id):
    # Delete repository
    task_id = deleteGit.request.id
    self.update_state(state = 'STARTED', meta = updateTask(task_id, username = started_by, status = 'started', progress = -1,
        message = 'Starting to delete repository "{}"'.format(repository_id)
    ))
    try:
        shutil.rmtree('{}/{}'.format(config['app']['lab_repository'], repository_id), ignore_errors = False)
    except Exception as err:
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to delete repository "{}" ({})'.format(repository_id, err),
            progress = 100
        )
    db.session.delete(RepositoryTable.query.get(repository_id))
    db.session.commit()
    return updateTask(
        task_id = task_id,
        username = started_by,
        status = 'completed',
        message = 'Repository "{}" successfully deleted'.format(repository_id),
        progress = 100
    )

@celery.task(bind = True)
def startNode(self, started_by, label, node_name, node_id, node_type, node_image, node_ip, router_id):
    # Start a node
    basic_auth = requests.auth.HTTPBasicAuth('admin', config['app']['api_key'])
    container_image = 'dainok/node-{}:{}'.format(node_type, node_image)
    container_name = 'node_{}'.format(label)
    task_id = startNode.request.id
    self.update_state(state = 'STARTED', meta = updateTask(task_id, username = started_by, status = 'started', progress = -1,
        message = 'Starting node "{}" (label {}) with image "{}"'.format(node_name, label, node_image)
    ))
    router = RouterTable.query.get(router_id)
    node = ActiveNodeTable.query.get(label)
    if not router:
        # Selected router does not exist
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to start node "{}" (label {}) on router_id "{}" (router does not exist)'.format(node_name, label, router_id),
            progress = 100
        )
    if router_id == 0:
        # Router is in the same network of controller
        router_ip = ipaddress.IPv4Interface(router.inside_ip).ip
        controller = config['app']['inside_ip']
    else:
        # Need to use the external IP
        router_ip = ipaddress.IPv4Interface(router.outside_ip).ip
        controller = config['app']['outside_ip']

    # Check node status
    r = requests.get('https://{}:5443/docker/containers/{}/json'.format(router_ip, container_name), verify = False, auth = basic_auth)
    if r.status_code == 404:
        # Selected container does not exist
        container_exists = False
    elif r.status_code == 200 and r.json()['State']['Running']:
        # Selected container is already running
        node.state = 'on'
        db.session.commit()
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to start node "{}" (label {}) on router_id "{}" (node is already running)'.format(node_name, label, router_id, node_image),
            progress = 100
        )
    elif r.status_code == 200:
        # Selected container exists
        container_exists = True
    else:
        # Failed to query Docker
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to start node "{}" (label {}) on router_id "{}" (cannot query Docker for container "{}", error {}: {})'.format(node_name, label, router_id, node_name, r.status_code, r.reason),
            progress = 100
        )

    # Check if node_image exists on Docker node
    r = requests.get('https://{}:5443/docker/images/{}/json'.format(router_ip, container_image), verify = False, auth = basic_auth)
    if r.status_code == 404:
        # Selected image does not exist
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to start node "{}" (label {}) on router_id "{}" (image "{}" does not exist)'.format(node_name, label, router_id, node_image),
            progress = 100
        )
    elif r.status_code != 200:
        # Failed to query Docker
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to start node "{}" (label {}) on router_id "{}" (cannot query Docker for image "{}", error {}: {})'.format(node_name, label, router_id, node_image, r.status_code, r.reason),
            progress = 100
        )

    if not container_exists:
        # Create container
        data = {
            'Env': [
                "CONTROLLER={}".format(controller),
                "LABEL={}".format(label)
            ],
            'HostConfig': {
                'Privileged': True
            },
            'Image': container_image,
        }
        r = requests.post('https://{}:5443/docker/containers/create?name={}'.format(router_ip, container_name), json = data, verify = False, auth = basic_auth)
        if r.status_code != 201:
            # Failed to query Docker
            return updateTask(
                task_id = task_id,
                username = started_by,
                status = 'failed',
                message = 'Failed to create node "{}" (label {}) on router_id "{}" (cannot query Docker, error {}: {})'.format(node_name, label, router_id, r.status_code, r.reason),
                progress = 100
            )

    # Start the node
    r = requests.post('https://{}:5443/docker/containers/{}/start'.format(router_ip, container_name), verify = False, auth = basic_auth)
    if r.status_code != 204:
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to start node "{}" (label {}) on router_id "{}" (cannot query Docker for start, error {}: {})'.format(node_name, label, router_id, r.status_code, r.reason),
            progress = 100
        )

    # Get node IP
    r = requests.get('https://{}:5443/docker/containers/{}/json'.format(router_ip, container_name), verify = False, auth = basic_auth)
    if r.status_code != 200:
        # Failed to query Docker
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to start node "{}" (label {}) on router_id "{}" (cannot query Docker for node IP, error {}: {})'.format(node_name, label, router_id, r.status_code, r.reason),
            progress = 100
        )
    node.state = 'on'
    node.ip = r.json()['NetworkSettings']['IPAddress']
    db.session.commit()

    return updateTask(
        task_id = task_id,
        username = started_by,
        status = 'completed',
        message = 'Node node "{}" started (label {}) on router_id "{}" with image "{}"'.format(node_name, label, router_id, node_image),
        progress = 100
    )

