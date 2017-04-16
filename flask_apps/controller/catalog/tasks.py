#!/usr/bin/env python3
""" Tasks """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

import os, sh, shutil
from controller import celery, config, git
from controller.catalog.models import *

@celery.task()
def addGit(repository, url, username, password):
    # Add a git repository for labs
    if os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository)):
        # Repository already exists
        print('Repository already "{}" exists'.format(repository))
        return False
    try:
        print('Starting to clone repository "{}" to "{}"'.format(url, repository))
        git.clone('-q', url, '{}/{}'.format(config['app']['lab_repository'], repository), _bg = False)
    except:
        print('Failed to clone repository "{}"'.format(url))
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
    return True

@celery.task()
def deleteGit(repository):
    # Delete repository
    print('Starting to delete repository "{}"'.format(repository))
    try:
        shutil.rmtree('{}/{}'.format(config['app']['lab_repository'], repository), ignore_errors = False)
    except:
        print('Failed to delete repository "{}"'.format(repository))
        return False
    print('Repository "{}" successfully deleted'.format(repository))
    return True
