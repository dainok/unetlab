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

def printLab(lab, summary = False):
    if summary:
        data =  {
            'id': lab.id,
            'name': lab.name,
            'repository': lab.repository,
            'author': lab.author,
            'version': lab.version
        }
    else:
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
        data = {
            'status': 'success',
            'message': 'User authenticated',
            'data': printUser(user)
        }
        data['data']['active_labs'] = {}
        for active_lab in user.active_labs:
            data['data']['active_labs'][active_lab.id] = {
                'id': active_lab.id,
                'name': active_lab.name,
                'repository': active_lab.repository,
                'author': active_lab.author,
                'version': active_lab.version
            }
        return data

class Lab(Resource):
    def delete(self, lab_id = None):
        username = checkAuthz(request)
        args = delete_lab_parser.parse_args()
        if not lab_id:
            # No lab has been selected
            abort(400)
        else:
            active_lab = ActiveLabTable.query.get((lab_id, username))
            lab = LabTable.query.get(lab_id)
        if not active_lab and not lab:
            abort(404)
        if active_lab:
            # If an active lab exists for the user, it can be deleted by the user himself
            db.session.delete(active_lab)
        if lab and args['commit'] == True:
            # If a lab exists, it can be deleted by an authorized user only
            checkAuthzPath(request, [lab.repository, lab.name], True)
            db.session.delete(lab)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Lab "{}" deleted'.format(lab_id)
        }

    def get(self, lab_id = None, page = 1):
        checkAuthz(request)
        if not lab_id:
            # List all labs
            labs = LabTable.query.paginate(page, 10).items
        else:
            # List a single lab if exists, else 404
            labs = [LabTable.query.get_or_404(lab_id)]
        data = {}
        for lab in labs:
            # Print each lab
            data[lab.id] = printLab(lab, summary = True)
        return {
            'status': 'success',
            'message': 'Role(s) found',
            'data': data
        }

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
        username = checkAuthzPath(request, [args['repository']], True)
        jlab = {
            'id': str(uuid.uuid4()),
            'name': args['name'],
            'repository': args['repository'],
            'author': args['author'],
            'version': args['version'],
            'topology': args['topology']
        }
        active_lab = ActiveLabTable(
            id = jlab['id'],
            name = jlab['name'],
            repository = jlab['repository'],
            author = jlab['author'],
            version = jlab['version'],
            json = json.dumps(jlab, separators = (',', ':'), sort_keys = True),
            username = username
        )
        db.session.add(active_lab)
        if args['commit']:
            # Write to file, add to git and commit
            lab_file = '{}/{}/{}.{}'.format(config['app']['lab_repository'], jlab['repository'], jlab['id'], config['app']['lab_extension'])
            lab = LabTable(
                id = jlab['id'],
                name = jlab['name'],
                repository = jlab['repository'],
                author = jlab['author'],
                version = jlab['version'],
                json = json.dumps(jlab, separators = (',', ':'), sort_keys = True),
            )
            with open(lab_file, 'w') as lab_fd:
                json.dump(printLab(lab), lab_fd, sort_keys = True, indent = 4)
            sh.git('-C', '{}/{}'.format(config['app']['lab_repository'], lab.repository), 'add', lab_file, _bg = False)
            sh.git('-C', '{}/{}'.format(config['app']['lab_repository'], lab.repository), 'commit', '-m', 'Added lab {} ("{}")'.format(lab.id, lab.name))
            db.session.add(lab)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Lab "{}" added'.format(active_lab.id),
            'data': printLab(active_lab)
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
            'data': printRole(role)
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
            'data': printRole(role)
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
            'data': printUser(user)
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
            'data': printUser(user)
        }
