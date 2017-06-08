#!/usr/bin/env python3
""" Tasks """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import os, sh, shutil
from controller import celery, config
from controller.catalog.models import *

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
    self.update_state(state='STARTED', meta = {
        'status': 'started',
        'message': 'Starting to clone repository "{}" from "{}"'.format(repository_id, url),
        'task': task_id,
        'progress': -1
    })
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
    self.update_state(state='STARTED', meta = {
        'status': 'started',
        'message': 'Starting to delete repository "{}"'.format(repository_id),
        'task': task_id,
        'progress': -1
    })
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
def startNode(self, label, name, node_id, type, image, router_id):
    # Start a node
    image = 'dainok/node-{}:{}'.format(type, image)
    task_id = startNode.request.id
    self.update_state(state='STARTED', meta = {
        'status': 'started',
        'message': 'Starting node "{}" (label {}) with image "{}"'.format(name, label, image),
        'task': task_id,
        'progress': -1
    })
    # check container
        # if not exist, create container, also if missing image
        # if exist, and not running, start container (where???)


