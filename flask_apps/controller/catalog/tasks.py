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
def addGit(self, started_by, repository, url, username, password):
    # Add a git repository for labs
    task_id = addGit.request.id
    self.update_state(state='STARTED', meta = {
        'status': 'started',
        'message': 'Starting to clone repository "{}" from "{}"'.format(repository, url),
        'task': task_id,
        'progress': -1
    })
    if os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository)):
        # Repository already exists
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Repository already "{}" exists'.format(repository),
            progress = 100
        )
    try:
        sh.git('-C', '{}'.format(config['app']['lab_repository']), 'clone', '-q', url, repository, _bg = False)
    except Exception as err:
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to clone repository "{}" from "{}" ({})'.format(repository, url, err),
            progress = 100
        )
    repository = RepositoryTable(
        id = repository,
        url = url,
        username = username,
        password = password
    )
    db.session.add(repository)
    db.session.commit()
    return updateTask(
        task_id = task_id,
        username = started_by,        status = 'completed',
        message = 'Repository "{}" successfully cloned from "{}"'.format(repository, url),
        progress = 100
    )

@celery.task(bind = True)
def deleteGit(self, started_by, repository):
    # Delete repository
    task_id = deleteGit.request.id
    self.update_state(state='STARTED', meta = {
        'status': 'started',
        'message': 'Starting to delete repository "{}"'.format(repository),
        'task': task_id,
        'progress': -1
    })
    try:
        shutil.rmtree('{}/{}'.format(config['app']['lab_repository'], repository), ignore_errors = False)
    except Exception as err:
        return updateTask(
            task_id = task_id,
            username = started_by,
            status = 'failed',
            message = 'Failed to delete repository "{}" ({})'.format(repository, err),
            progress = 100
        )
    db.session.delete(RepositoryTable.query.get(repository))
    db.session.commit()
    return updateTask(
        task_id = task_id,
        username = started_by,
        status = 'completed',
        message = 'Repository "{}" successfully deleted'.format(repository),
        progress = 100
    )

