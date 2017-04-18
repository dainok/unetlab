#!/usr/bin/env python3
""" Tasks """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

import os, sh, shutil
from controller import celery, config
from controller.catalog.models import *

@celery.task()
def addGit(repository, url, username, password):
    # Add a git repository for labs
    task = addGit.request.id
    if os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository)):
        # Repository already exists
        print('Repository already "{}" exists'.format(repository))
        print('Task {} failed'.format(task))
        return False
    try:
        print('Starting to clone repository "{}" to "{}"'.format(url, repository))
        sh.git('-C', '{}'.format(config['app']['lab_repository']), 'clone', '-q', url, repository, _bg = False)
    except Exception as err:
        print('Failed to clone repository "{}"'.format(url))
        print('Task {} failed'.format(task))
        print(err)
        return False
    repository = RepositoryTable(
        repository = repository,
        url = url,
        username = username,
        password = password
    )
    db.session.add(repository)
    db.session.commit()
    print('Repository "{}" successfully cloned'.format(url))
    print('Task {} completed'.format(task))
    return True

@celery.task()
def deleteGit(repository):
    # Delete repository
    task = deleteGit.request.id
    print('Starting to delete repository "{}"'.format(repository))
    try:
        shutil.rmtree('{}/{}'.format(config['app']['lab_repository'], repository), ignore_errors = False)
    except Exception as err:
        print('Failed to delete repository "{}"'.format(repository))
        print('Task {} failed'.format(task))
        print(err)
        return False
    db.session.delete(RepositoryTable.query.get(repository))
    db.session.commit()
    print('Repository "{}" successfully deleted'.format(repository))
    print('Task {} completed'.format(task))
    return True
