#!/usr/bin/env python3
""" Tasks """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

import os, sh, shutil
from controller import celery, config
from controller.catalog.models import *

@celery.task(bind = True)
def addGit(repository, url, username, password):
    # Add a git repository for labs
    task = addGit.request.id
    self.update_state(state='STARTED', meta={
        'status': 'started',
        'message': 'Starting to clone repository "{}"'.format(repository),
        'task': task,
        'progress': -1
    })
    if os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository)):
        # Repository already exists
        return {
            'status': 'failed',
            'message': 'Repository already "{}" exists'.format(repository),
            'task': task,
            'progress': -1
        }
    try:
        sh.git('-C', '{}'.format(config['app']['lab_repository']), 'clone', '-q', url, repository, _bg = False)
    except Exception as err:
        return {
            'status': 'failed',
            'message': 'Failed to clone repository "{}" ({})'.format(url, err),
            'task': task,
            'progress': -1
        }
    repository = RepositoryTable(
        repository = repository,
        url = url,
        username = username,
        password = password
    )
    db.session.add(repository)
    db.session.commit()
    return {
        'status': 'completed',
        'message': 'Repository "{}" successfully cloned'.format(url),
        'task': task,
        'progress': -1
    }

@celery.task(bind = True)
def deleteGit(repository):
    # Delete repository
    task = deleteGit.request.id
    self.update_state(state='STARTED', meta={
        'status': 'started',
        'message': 'Starting to delete repository "{}"'.format(repository),
        'task': task,
        'progress': -1
    })
    try:
        shutil.rmtree('{}/{}'.format(config['app']['lab_repository'], repository), ignore_errors = False)
    except Exception as err:
        return {
            'status': 'failed',
            'message': 'Failed to delete repository "{}" ({})'.format(url, err),
            'task': task,
            'progress': -1
        }
    db.session.delete(RepositoryTable.query.get(repository))
    db.session.commit()
    return {
        'status': 'completed',
        'message': 'Repository "{}" successfully deleted'.format(repository),
        'task': task,
        'progress': -1
    }

