#!/usr/bin/env python3
""" Resources """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

import json, os, shutil, uuid
from flask import abort, request
from flask_restful import Resource
from controller import cache, config
from controller.catalog.aaa import checkAuth, checkAuthz, checkAuthzPath
from controller.catalog.models import *
from controller.catalog.parsers import *
from controller.catalog.tasks import *

def printLab(lab):
    data = json.loads(lab.json)
    return data

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

class Lab(Resource):
    # TODO: post
    # creo nuovo lab: creo il file nel repository, se non esiste
    # lo modifico, e' in db fino al save
    # save, scrivo in git e commit + push?
    # TODO: patch
    # modifico in DB
    # TODO: delete
    # cancello da DB e da repo
    def post(self):
        args = add_lab_parser.parse_args()
        checkAuthzPath(request, [args['repository']], True)
        jlab = {
            'id': str(uuid.uuid4()),
            'name': args['name'],
            'repository': args['repository'],
            'author': args['author'],
            'version': args['version']
        }
        lab = LabTable(
            id = jlab['id'],
            name = jlab['name'],
            repository = jlab['repository'],
            author = jlab['author'],
            version = jlab['version'],
            json = json.dumps(jlab, separators=(',', ':'), sort_keys = True)
        )
        db.session.add(lab)
        db.session.commit()
        if args['commit']:
            # TODO: manage exception: delete lab, remove from db only if commit = true
            # Write to file, add to git and commit
            lab_file = '{}/{}/{}.{}'.format(config['app']['lab_repository'], lab.repository, lab.id, config['app']['lab_extension'])
            with open(lab_file, 'w') as lab_fd:
                json.dump(printLab(lab), lab_fd, sort_keys = True, indent = 4)
            sh.git('-C', '{}/{}'.format(config['app']['lab_repository'], lab.repository), 'add', lab_file, _bg = False)
            sh.git('-C', '{}/{}'.format(config['app']['lab_repository'], lab.repository), 'commit', '-m', 'Added lab {} ("{}")'.format(lab.id, lab.name))
        return {
            'status': 'success',
            'message': 'Lab "{}" added'.format(lab.id),
            'data': {
                lab.id: printLab(lab)
            }
        }

class Repository(Resource):
    # TODO: only admin edit remote
    # TODO: all users with write permission push
    # TODO: all users with write permission commit -> solo se un lab viene salvato (i lab vengono caricati e messi su in db. editati da db. solo save li porta sul repo con commit)
    # TODO: all users with write permission pull
    # TODO: allo startup pull + scan dei repo con aggiunta al db dei lab
    def delete(self, repository = None):
        checkAuthz(request, ['admin'])
        if not repository:
            # No repository has been selected
            abort(400)
        elif repository == 'local':
            # Repository 'local' cannot be deleted
            abort(403)
        elif not os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository)):
            # Repository does not exist
            abort(404)
        t = deleteGit.apply_async((repository,))
        return {
            'status': 'enqueued',
            'message': 'Task "{}" enqueued to the batch manager'.format(t),
            'task': str(t)
        }

    def post(self):
        args = add_repository_parser.parse_args()
        checkAuthz(request, ['admin'])
        if args['repository'] == 'local':
            # local is a reserved repository
            abort(400)
        t = addGit.apply_async((args['repository'], args['url'], args['username'], args['password']))
        return {
            'status': 'enqueued',
            'message': 'Task "{}" enqueued to the batch manager'.format(t),
            'task': str(t)
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
        args = patch_role_parser.parse_args()
        checkAuthz(request, ['admin'])
        if not role:
            # No role has been selected
            abort(400)
        else:
            # Get the role if exists, else 404
            role = RoleTable.query.get_or_404(role)
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
        args = add_role_parser.parse_args()
        checkAuthz(request, ['admin'])
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
        args = patch_user_parser.parse_args()
        checkAuthz(request, ['admin'])
        if not username:
            # No user has been selected
            abort(400)
        else:
            # Get the user if exists, else 404
            user = UserTable.query.get_or_404(username)
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
        args = add_user_parser.parse_args()
        checkAuthz(request, ['admin'])
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
