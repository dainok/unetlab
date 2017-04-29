#!/usr/bin/env python3
""" Resources """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170429'

import hashlib, json, os, shutil, uuid
from flask import abort, request
from flask_restful import Resource
from controller import cache, config
from controller.catalog.aaa import checkAuth, checkAuthz, checkAuthzPath
from controller.catalog.models import *
from controller.catalog.parsers import *
from controller.catalog.tasks import *

def activateLab(username, jlab):
    # Checking for available labels
    available_labels = getAvailableLabels(username)
    if available_labels != -1 and available_labels < len(jlab['topology']['nodes']):
        abort(403)
    # Make the lab active
    active_lab = ActiveLabTable(
        id = jlab['id'],
        name = jlab['name'],
        repository_id = jlab['repository'],
        author = jlab['author'],
        version = jlab['version'],
        json = json.dumps(jlab, separators = (',', ':'), sort_keys = True),
        username = username,
        instance = str(uuid.uuid4())
    )
    db.session.add(active_lab)
    db.session.commit()
    # Setting labels
    label = 0
    connections = {}
    for node_id, node in jlab['topology']['nodes'].items():
        while ActiveNodeTable.query.get(label) != None:
            label = label + 1
        active_lab.nodes.append(ActiveNodeTable(
            node_id = node_id,
            state = 'off',
            label = label
        ))
        for interface_id, interface in node['interfaces'].items():
            if not interface['connection'] in connections:
                connections[interface['connection']] = []
            connections[interface['connection']].append({
                'node_id': node_id,
                'label': label,
                'interface_id': interface_id
            })
    db.session.commit()
    # Setting connections
    for connection_id, connection in connections.items():
        if len(connection) == 2:
            # Evaluating only valid P2P connections
            db.session.add(ActiveInterfaceTable(
                id = connection[0]['interface_id'],
                label = connection[0]['label'],
                dst_label = connection[1]['label'],
                dst_if = connection[1]['interface_id']
            ))
            db.session.add(ActiveInterfaceTable(
                id = connection[1]['interface_id'],
                label = connection[1]['label'],
                dst_label = connection[0]['label'],
                dst_if = connection[0]['interface_id']
            ))
            db.session.commit()

def getAvailableLabels(username):
    # Return available labels for a specific user
    max_labels = UserTable.query.get_or_404(username).labels
    used_labels = 0
    for active_lab in UserTable.query.get_or_404(username).active_labs:
        used_labels = used_labels + len(active_lab.nodes)
    if max_labels == -1:
        return max_labels
    return max_labels - used_labels

def printController(controller):
    return {
        'id': controller.id,
        'inside_ip': controller.inside_ip,
        'outside_ip': controller.outside_ip,
        'master': controller.master,
        'docker_ip': controller.docker_ip
    }

def printLab(lab, summary = False):
    if summary:
        data =  {
            'id': lab.id,
            'name': lab.name,
            'repository': lab.repository_id,
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

def printTask(task):
    return {
        'id': task.id,
        'status': task.status,
        'message': task.message,
        'progress': task.progress,
        'username': task.username
    }

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
                'repository': active_lab.repository_id,
                'author': active_lab.author,
                'version': active_lab.version
            }
        return data

class Controller(Resource):
    def get(self, controller_id = None, page = 1):
        checkAuthz(request, ['admin'])
        if not controller_id:
            # List all controllers
            controllers = ControllerTable.query.paginate(page, 10).items
        else:
            # List a single controller if exists, else 404
            controllers = ControllerTable.query.get_or_404(controller_id)
        data = {}
        for controller in controllers:
            # Print each controller
            data[controller.id] = printController(controller)
        return {
            'status': 'success',
            'message': 'Controller(s) found',
            'data': data
        }

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
            checkAuthzPath(request, [lab.repository_id, lab.name], True)
            db.session.delete(lab)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Lab "{}" deleted'.format(lab_id)
        }

    def get(self, lab_id = None, page = 1):
        username = checkAuthz(request)
        if not lab_id:
            # List all labs
            summary = True
            labs = LabTable.query.paginate(page, 10).items
        else:
            # List a single lab if exists, else 404
            summary = False
            active_lab = ActiveLabTable.query.get((lab_id, username))
            lab = LabTable.query.get(lab_id)
            if active_lab:
                # Found an active lab
                labs = [active_lab]
            elif lab:
                # Found a lab
                labs = [lab]
                jlab = json.loads(lab.json)
                # Make the lab active
                activateLab(username, jlab)
            else:
                abort(404)
        data = {}
        for lab in labs:
            # Print each lab
            data[lab.id] = printLab(lab, summary = summary)
        return {
            'status': 'success',
            'message': 'Lab(s) found',
            'data': data
        }

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
        # Make the lab active
        activateLab(username, jlab)
        if args['commit']:
            # Write to file, add to git and commit
            lab_file = '{}/{}/{}.{}'.format(config['app']['lab_repository'], jlab['repository'], jlab['id'], config['app']['lab_extension'])
            lab = LabTable(
                id = jlab['id'],
                name = jlab['name'],
                repository_id = jlab['repository'],
                author = jlab['author'],
                version = jlab['version'],
                json = json.dumps(jlab, separators = (',', ':'), sort_keys = True),
            )
            with open(lab_file, 'w') as lab_fd:
                json.dump(printLab(lab), lab_fd, sort_keys = True, indent = 4)
            sh.git('-C', '{}/{}'.format(config['app']['lab_repository'], lab.repository_id), 'add', lab_file, _bg = False)
            sh.git('-C', '{}/{}'.format(config['app']['lab_repository'], lab.repository_id), 'commit', '-m', 'Added lab {} ("{}")'.format(lab.id, lab.name))
            db.session.add(lab)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Lab "{}" added'.format(lab.id),
            'data': printLab(lab)
        }

class Repository(Resource):
    # TODO: only admin edit remote
    # TODO: all users with write permission push
    # TODO: all users with write permission commit -> solo se un lab viene salvato (i lab vengono caricati e messi su in db. editati da db. solo save li porta sul repo con commit)
    # TODO: all users with write permission pull
    # TODO: allo startup pull + scan dei repo con aggiunta al db dei lab
    def delete(self, repository = None):
        username = checkAuthz(request, ['admin'])
        if not repository:
            # No repository has been selected
            abort(400)
        elif repository == 'local':
            # Repository 'local' cannot be deleted
            abort(403)
        elif not os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository)):
            # Repository does not exist
            abort(404)
        t = deleteGit.apply_async((username, repository,))
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
        t = addGit.apply_async((username, args['repository'], args['url'], args['username'], args['password']))
        return {
            'status': 'enqueued',
            'message': 'Task "{}" enqueued to the batch manager'.format(t),
            'task': str(t)
        }

class Routing(Resource):
    def get(self, role = None, page = 1):
        checkAuthz(request, ['admin'])
        nodes = ActiveNodeTable.query
        controllers = []
        for controller in ControllerTable.query:
            controllers.append(controller.id)
        node_controllers = {}
        for node in nodes:
            node_controller = 0 if node.controller_id not in controllers else node.controller_id
            node_controllers[node.label] = node_controller

        data = []
        for node in nodes:
            src_label = node.label
            for interface in node.interfaces:
                route = {
                    'src_label': node.label,
                    'src_if': interface.id,
                    'dst_controller': node_controllers[interface.dst_label],
                    'dst_label': interface.dst_label,
                    'dst_if' : interface.dst_if
                }
            data.append(route)
        return {
            'status': 'success',
            'message': 'Routing table found',
            'data': data
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

class Task(Resource):
    def get(self, task_id = None, page = 1):
        username = checkAuthz(request)
        if not task_id:
            # List all tasks
            # TODO from this user only, or all for admins
            tasks = TaskTable.query.paginate(page, 10).items
        else:
            # List a single task if exists, else 404
            # TODO task can be pending: see https://blog.miguelgrinberg.com/post/using-celery-with-flask (task = long_task.AsyncResult(task_id))
            tasks = [TaskTable.query.get_or_404(task_id)]
        data = {}
        for task in tasks:
            # Print each task
            data[task.id] = printTask(task)
        return {
            'status': 'success',
            'message': 'Task(s) found',
            'data': data
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
