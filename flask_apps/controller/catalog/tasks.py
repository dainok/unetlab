#!/usr/bin/env python3
""" Tasks """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from controller import celery

@celery.task()
def add_together(a, b):
    return a + b
