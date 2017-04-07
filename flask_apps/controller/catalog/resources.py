#!/usr/bin/env python3
""" Resources """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from flask import request
from flask_restful import Resource
from controller.catalog.aaa import checkAuth, checkAuthz
from controller.catalog.models import *
from controller.catalog.parsers import *

class User(Resource):
    def get(self, username = None, page = 1):
        checkAuthz(request, 'admin')
        if not username:
            # List all users
            users = UserTable.query.paginate(page, 10).items
        else:
            # List a single user if exists, else 404
            users = [ UserTable.query.get_or_404(username) ]
        data = {}
        for user in users:
            # Print each user and roles
            data[user.username] = {
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'labels': user.labels,
                'roles': []
            }
            for role in user.roles:
                data[user.username]['roles'].append(role.role)
        return {
            'status': 'success',
            'data': data
        }
    def post(self):
        args = user_parser.parse_args(strict=True)
        user = {
            'username': args['username'],
            'password': args['password'],
            'name': args['name'],
            'email': args['email'],
            'labels': args['labels'],
            'roles': args['roles']
        }
        return {
            'status': 'success',
        }
