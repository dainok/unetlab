#!/usr/bin/env python3
""" Resources """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from flask import abort, request
from flask_restful import Resource
from controller import cache
from controller.catalog.aaa import checkAuth, checkAuthz
from controller.catalog.models import *
from controller.catalog.parsers import *

def printRole(role):
    return {
        'role': role.role,
        'access_to': role.access_to,
        'can_write': role.can_write
    }

def printUser(user):
    data = {
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'labels': user.labels,
        'roles': []
    }
    for role in user.roles:
        data['roles'].append(role.role)
    return data

class Auth(Resource):
    def get(self):
        user = UserTable.query.get_or_404(checkAuthz(request))
        return {
            'status': 'success',
            'message': 'User authenticated',
            'data': printUser(user)
        }

class Role(Resource):
    def delete(self, role = None):
        checkAuthz(request, ['admin'])
        if not role:
            # No role has been selected
            abort(400)
        elif role == 'admin':
            # Role 'admin' cannot be deleted
            abort(403)
        else:
            # Get the role if exists, else 404
            role = RoleTable.query.get_or_404(role)
        db.session.delete(role)
        db.session.commit()
        for user in role.users:
            # Purging the cached user
            cache.delete(user.username)
        return {
            'status': 'success',
            'message': 'Role "{}" deleted'.format(role.role)
        }

    def get(self, role = None, page = 1):
        checkAuthz(request, ['admin'])
        if not role:
            # List all roles
            roles = RoleTable.query.paginate(page, 10).items
        else:
            # List a single role if exists, else 404
            roles = [RoleTable.query.get_or_404(role)]
        data = {}
        for role in roles:
            # Print each role
            data[role.role] = printRole(role)
        return {
            'status': 'success',
            'message': 'Role(s) found',
            'data': data
        }

    def patch(self, role = None):
        checkAuthz(request, ['admin'])
        if not role:
            # No role has been selected
            abort(400)
        else:
            # Get the role if exists, else 404
            role = RoleTable.query.get_or_404(role)
        args = patch_role_parser.parse_args()
        for key, value in args.items():
            if key in ['access_to', 'can_write']:
                setattr(role, key, value)
        db.session.commit()
        for user in role.users:
            # Purging the cached user
            cache.delete(user.username)
        return {
            'status': 'success',
            'message': 'Role "{}" saved'.format(role.role),
            'data': {
                role.role: printRole(role)
            }
        }

    def post(self):
        checkAuthz(request, ['admin'])
        args = add_role_parser.parse_args()
        if RoleTable.query.get(args['role']):
            # Role eady exists
            abort(409)
        role = RoleTable(
            role = args['role'],
            can_write = args['can_write'],
            access_to = args['access_to']
        )
        db.session.add(role)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Role "{}" added'.format(role.role),
            'data': {
                role.role: printRole(role)
            }
        }

class User(Resource):
    def delete(self, username = None):
        checkAuthz(request, ['admin'])
        if not username:
            # No user has been selected
            abort(400)
        elif username == 'admin':
            # User 'admin' cannot be deleted
            abort(403)
        else:
            # Get the user if exists, else 404
            user = UserTable.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        # Purging the cached user
        cache.delete(user.username)
        return {
            'status': 'success',
            'message': 'User "{}" deleted'.format(user.username)
        }

    def get(self, username = None, page = 1):
        checkAuthz(request, ['admin'])
        if not username:
            # List all users
            users = UserTable.query.paginate(page, 10).items
        else:
            # List a single user if exists, else 404
            users = [UserTable.query.get_or_404(username)]
        data = {}
        for user in users:
            # Print each user
            data[user.username] = printUser(user)
        return {
            'status': 'success',
            'message': 'User(s) found',
            'data': data
        }

    def patch(self, username = None):
        checkAuthz(request, ['admin'])
        if not username:
            # No user has been selected
            abort(400)
        else:
            # Get the user if exists, else 404
            user = UserTable.query.get_or_404(username)
        args = patch_user_parser.parse_args()
        for key, value in args.items():
            if key in ['email', 'labels', 'name']:
                setattr(user, key, value)
            if key == 'password':
                setattr(user, key, hashlib.sha256(value.encode('utf-8')).hexdigest())
            if key == 'roles':
                # Removing previous roles and add new ones
                user.roles = []
                for role in value:
                    user.roles.append(RoleTable.query.get_or_404(role))
        db.session.commit()
        # Purging the cached user
        cache.delete(user.username)
        return {
            'status': 'success',
            'message': 'User "{}" saved'.format(user.username),
            'data': {
                user.username: printUser(user)
            }
        }

    def post(self):
        checkAuthz(request, ['admin'])
        args = add_user_parser.parse_args()
        if UserTable.query.get(args['username']):
            # User already exists
            abort(409)
        user = UserTable(
            username = args['username'],
            password = hashlib.sha256(args['password'].encode('utf-8')).hexdigest(),
            name = args['name'],
            email = args['email'],
            labels = args['labels']
        )
        user.roles = []
        for role in args['roles']:
            # Adding all roles
            user.roles.append(RoleTable.query.get_or_404(role))
        db.session.add(user)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'User "{}" added'.format(user.username),
            'data': {
                user.username: printUser(user)
            }
        }

