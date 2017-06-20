#!/usr/bin/env python3
""" Data parsers """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import ipaddress, os, validate_email
from flask import abort, jsonify, make_response, request
from controller import config
from controller.catalog.models import *

# Parser for arguments

def parse_email(email):
    email = parse_type(email, 'email', str)
    if not validate_email.validate_email(email):
        abort(make_response(jsonify(message = 'Argument "email" is not valid'), 400))
    return email

def parse_ip(ip):
    try:
        ip = ipaddress.ip_address(ip)
    except:
        abort(make_response(jsonify(message = 'Argument "ip" is invalid'), 400))
    return ip

def parse_json():
    rargs = request.json
    if not rargs:
        abort(make_response(jsonify(message = 'Input data is not a valid JSON'), 400))
    return rargs

def parse_label(label):
    # A label must be integer greater than -1
    label = parse_type(label, 'label', int)
    if label < 0:
        abort(make_response(jsonify(message = 'Argument "label" must be equal or greater than 0'), 400))
    return label

def parse_labels(labels):
    # A label must be integer greater than -1 (-1 is infinite)
    labels = parse_type(labels, 'labels', int)
    if labels < -1:
        abort(make_response(jsonify(message = 'Argument "labels" must be equal or greater than -1'), 400))
    return labels

def parse_password(password):
    password = parse_type(password, 'password', str)
    if password == '':
        abort(make_response(jsonify(message = 'Argument "password" cannot be empty'), 400))
    return password

def parse_repository(repository):
    if not RepositoryTable.query.get(repository):
        abort(make_response(jsonify(message = 'Argument "repository" is invalid'), 400))
    return repository

def parse_roles(roles):
    roles = parse_type(roles, 'roles', list)
    for role in roles:
        if not RoleTable.query.get(role):
            abort(make_response(jsonify(message = 'Role "{}" not found'.format(role)), 400))
    return roles

def parse_state(state):
    # State can be "on" or "off"
    if state != 'on' and state != 'off':
        abort(make_response(jsonify(message = 'Argument "state" is invalid'), 400))
    return state

def parse_topology(topology):
    topology = parse_type(topology, 'topology', dict)

    if 'nodes' in topology:
        nodes = parse_type(topology['nodes'], 'topology[nodes]', dict)
        for node_id, node in nodes.items():
            if not node_id.isdigit():
                abort(make_response(jsonify(message = 'Argument node_id in "topology[nodes][node_id]" must be numeric'), 400))
            node = parse_type(node, 'topology[nodes][{}]'.format(node_id), dict)
            if 'interfaces' in node:
                interfaces = parse_type(node['interfaces'], 'topology[nodes][{}][interfaces]'.format(node_id), dict)
                for interface_id, interface in node['interfaces'].items():
                    if not interface_id.isdigit():
                        abort(make_response(jsonify(message = 'Argument interface_id in "topology[nodes][interfaces][interface_id]" must be numeric'), 400))
                    interface = parse_type(interface, 'topology[nodes][{}][interfaces][{}]'.format(node_id, interface_id), dict)
    else:
        topology['nodes'] = {}

    if 'connections' in topology:
        connections = parse_type(topology['connections'], 'topology[connections]', dict)
        for connection_id, connection in connections.items():
            if not connection_id.isdigit():
                abort(make_response(jsonify(message = 'Argument connection_id in "topology[connections][connection_id]" must be numeric'), 400))
            connection = parse_type(connection, 'topology[connections][{}]'.format(connection_id), dict)
    else:
        topology['connections'] = {}
    
    return topology

def parse_type(arg, arg_name, arg_type):
    if not isinstance(arg, arg_type):
        abort(make_response(jsonify(message = 'Argument "{}" must be "{}"'.format(arg_name, arg_type)), 400))
    return arg

# Parser for DELETE/GET/PATCH/POST

def auth_parser_patch(username):
    args = {}
    rargs = parse_json()

    if not UserTable.query.get(parse_type(username, 'username', str)):
        abort(make_response(jsonify(message = 'Username "{}" not found'.format(username)), 404))

    if 'password' in rargs: 
        args['password'] = parse_password(rargs['password'])
    else:
        abort(make_response(jsonify(message = 'Argument "password" is not valid'), 400))

    return args

def lab_parser_delete(lab_id, username = None):
    args = {}

    active_lab = ActiveLabTable.query.get((lab_id, username))
    lab = LabTable.query.get(lab_id)
    if request.args.get('commit') == 'true':
        args['commit'] = True
    else:
        args['commit'] = False

    if not active_lab and not lab:
        abort(make_response(jsonify(message = 'Lab "{}" not found').format(lab_id), 404))

    return args

def lab_parser_get(lab_id):
    active_lab = ActiveLabTable.query.get((lab_id, username))
    lab = LabTable.query.get(lab_id)

    if not active_lab and not lab:
        abort(make_response(jsonify(message = 'Lab "{}" not found').format(lab_id), 404))

def lab_parser_patch(lab_id):
    args = {}
    rargs = parse_json()

    active_lab = ActiveLabTable.query.get((lab_id, username))
    lab = LabTable.query.get(lab_id)
    if request.args.get('commit') == 'true':
        args['commit'] = True
    else:
        args['commit'] = False

    if not active_lab and not lab:
        abort(make_response(jsonify(message = 'Lab "{}" not found').format(lab_id), 404))

    if 'author' in rargs:
        args['author'] = parse_type(rargs['author'], 'author', str)

    if 'name' in rargs and rargs['name'] != '':
        args['name'] = parse_type(rargs['name'], 'name', str)
    else:
        abort(make_response(jsonify(message = 'Argument "name" cannot be blank'), 400))

    if 'topology' in rargs:
        args['topology'] = parse_topology(rargs['topology'])

    if 'version' in rargs:
        args['version'] = parse_type(rargs['version'], 'version', int)

    return args

def lab_parser_post():
    args = {}
    rargs = parse_json()

    if request.args.get('commit') == 'true':
        args['commit'] = True
    else:
        args['commit'] = False

    if 'author' in rargs:
        args['author'] = parse_type(rargs['author'], 'author', str)
    else:
        args['author'] = ''

    if 'name' in rargs and rargs['name'] != '':
        args['name'] = parse_type(rargs['name'], 'name', str)
    else:
        abort(make_response(jsonify(message = 'Argument "name" cannot be blank'), 400))

    if 'repository' in rargs:
        args['repository'] = parse_repository(rargs['repository'])
    else:
        abort(make_response(jsonify(message = 'Argument "repository" cannot be blank'), 400))

    if 'topology' in rargs:
        args['topology'] = parse_topology(rargs['topology'])
    else:
        abort(make_response(jsonify(message = 'Argument "topology" cannot be blank'), 400))

    if 'version' in rargs:
        args['version'] = parse_type(rargs['version'], 'version', int)
    else:
        args['version'] = 0

    return args

def node_parser_patch(label):
    args = {}
    rargs = parse_json()

    if not ActiveNodeTable.query.get(parse_label(label)):
        abort(make_response(jsonify(message = 'Argument "label" cannot be blank'), 400))

    if 'ip' in rargs:
        args['ip'] = parse_ip(rargs['ip'])
    else:
        abort(make_response(jsonify(message = 'Argument "ip" cannot be blank'), 400))

    if 'state' in rargs:
        args['state'] = parse_state(rargs['state'])
    else:
        abort(make_response(jsonify(message = 'Argument "state" cannot be blank'), 400))

    return args

def repository_parser_delete(repository_id):
    if repository_id == 'local':
        abort(make_response(jsonify(message = 'Cannot delete repository "local"'), 403))

    if not RepositoryTable.query.get(parse_type(repository_id, 'id', str)):
        abort(make_response(jsonify(message = 'Repository "{}" not found').format(repository_id), 404))

def repository_parser_get(repository_id):
    if not RepositoryTable.query.get(parse_type(repository_id, 'id', str)):
        abort(make_response(jsonify(message = 'Repository "{}" not found').format(repository_id), 404))

def repository_parser_patch(repository_id):
    args = {}
    rargs = parse_json()

    if not RepositoryTable.query.get(parse_type(repository_id, 'id', str)):
        abort(make_response(jsonify(message = 'Repository "{}" not found').format(repository_id), 404))

    if 'password' in rargs: 
        args['password'] = parse_password(rargs['password'])

    if 'url' in rargs: 
        args['url'] = parse_type(rargs['url'], 'username', str)

    if 'username' in rargs: 
        args['username'] = parse_type(rargs['username'], 'username', str)

    return args

def repository_parser_post():
    args = {}
    rargs = parse_json()

    if 'repository' in rargs:
        if RepositoryTable.query.get(parse_type(rargs['repository'], 'id', str)):
            abort(make_response(jsonify(message = 'Repository "{}" not found').format(repository_id), 404))
        args['repository'] = rargs['repository']
    else:
        abort(make_response(jsonify(message = 'Argument "repository" cannot be blank'), 400))

    if 'password' in rargs: 
        args['password'] = parse_password(rargs['password'])
    else:
        args['password'] = ''

    if 'repository' in rargs:
        if RepositoryTable.query.get(parse_type(rargs['repository'], 'repository', str)):
            abort(make_response(jsonify(message = 'Repository "{}" already exists'.format(rargs['repository'])), 409))
        args['repository'] = rargs['repository']
    else:
        abort(make_response(jsonify(message = 'Argument "repository" cannot be blank'), 400))

    if 'url' in rargs: 
        args['url'] = parse_type(rargs['url'], 'url', str)
    else:
        abort(make_response(jsonify(message = 'Argument "url" cannot be blank'), 400))

    if 'username' in rargs: 
        args['username'] = parse_type(email, 'username', str)
    else:
        args['username'] = ''
        
    return args

def role_parser_delete(role):
    if role == 'admin':
        abort(make_response(jsonify(message = 'Cannot delete role "admin"'), 403))
    elif not RoleTable.query.get(parse_type(role, 'role', str)):
        abort(make_response(jsonify(message = 'Role "{}" not found').format(role), 404))

def role_parser_get(role):
    if not RoleTable.query.get(parse_type(role, 'role', str)):
        abort(make_response(jsonify(message = 'Role "{}" not found').format(role), 404))

def role_parser_patch(role):
    args = {}
    rargs = parse_json()

    if not RoleTable.query.get(parse_type(role, 'role', str)):
        abort(make_response(jsonify(message = 'Role "{}" not found'.format(role)), 404))

    if 'access_to' in rargs: 
        args['access_to'] = parse_type(rargs['access_to'], 'access_to', str)

    if 'can_write' in rargs: 
        args['can_write'] = parse_type(rargs['can_write'], 'can_write', bool)

    return args
        
def role_parser_post():
    args = {}
    rargs = parse_json()

    if 'access_to' in rargs: 
        args['access_to'] = parse_type(rargs['access_to'], 'access_to', str)
    else:
        args['access_to'] = ''

    if 'can_write' in rargs: 
        args['can_write'] = parse_type(rargs['can_write'], 'can_write', bool)
    else:
        args['can_write'] = False

    if 'role' in rargs:
        if RoleTable.query.get(parse_type(rargs['role'], 'role', str)):
            abort(make_response(jsonify(message = 'Role "{}" already exists'.format(rargs['role'])), 409))
        args['role'] = rargs['role']
    else:
        abort(make_response(jsonify(message = 'Argument "role" cannot be blank'), 400))

    return args
        
def router_parser_delete(router_id):
    if not RouterTable.query.get(parse_type(router_id, 'id', int)):
        abort(make_response(jsonify(message = 'Router "{}" not found').format(router_id), 404))

def router_parser_get(router_id):
    if not RouterTable.query.get(parse_type(router_id, 'id', int)):
        abort(make_response(jsonify(message = 'Router "{}" not found').format(router_id), 404))

def router_parser_patch(router_id):
    args = {}
    rargs = parse_json()

    if not RouterTable.query.get(parse_type(router_id, 'id', int)):
        abort(make_response(jsonify(message = 'Router "{}" not found').format(router_id), 404))

    if 'inside_ip' in rargs: 
        args['inside_ip'] = parse_ip(rargs['inside_ip'])

    if 'outside_ip' in rargs: 
        args['outside_ip'] = parse_ip(rargs['outside_ip'])

    return args

def router_parser_post():
    args = {}
    rargs = parse_json()

    if 'id' in rargs:
        if RouterTable.query.get(parse_type(rargs['id'], 'id', int)):
            abort(make_response(jsonify(message = 'Router "{}" already exists'.format(rargs['id'])), 409))
        args['id'] = rargs['id']
    else:
        abort(make_response(jsonify(message = 'Argument "id" cannot be blank'), 400))

    if 'inside_ip' in rargs: 
        args['inside_ip'] = parse_ip(rargs['inside_ip'])
    else:
        abort(make_response(jsonify(message = 'Argument "inside_ip" cannot be blank'), 400))

    if 'outside_ip' in rargs: 
        args['outside_ip'] = parse_ip(rargs['outside_ip'])
    else:
        args['outside_ip'] = '0.0.0.0'

    return args

def user_parser_delete(username):
    if username == 'admin':
        abort(make_response(jsonify(message = 'Cannot delete username "admin"'), 403))
    elif not UserTable.query.get(parse_type(username, 'username', str)):
        abort(make_response(jsonify(message = 'Username "{}" not found').format(username), 404))

def user_parser_get(username):
    if not UserTable.query.get(parse_type(username, 'username', str)):
        abort(make_response(jsonify(message = 'Username "{}" not found').format(username), 404))

def user_parser_patch(username):
    args = {}
    rargs = parse_json()

    if not UserTable.query.get(parse_type(username, 'username', str)):
        abort(make_response(jsonify(message = 'Username "{}" not found').format(username), 404))

    if 'email' in rargs: 
        args['email'] = parse_email(rargs['email'])

    if 'labels' in rargs: 
        args['labels'] = parse_labels(rargs['labels'])

    if 'name' in rargs: 
        args['name'] = parse_type(rargs['name'], 'name', str)

    if 'password' in rargs: 
        args['password'] = parse_type(rargs['password'], 'password', str)

    if 'roles' in rargs: 
        args['roles'] = parse_roles(rargs['roles'])

    return args

def user_parser_post():
    args = {}
    rargs = parse_json()

    if 'email' in rargs: 
        args['email'] = parse_email(rargs['email'])
    else:
        abort(make_response(jsonify(message = 'Argument "email" cannot be blank'), 400))

    if 'labels' in rargs: 
        args['labels'] = parse_labels(rargs['labels'])
    else:
        args['labels'] = 0

    if 'name' in rargs: 
        args['name'] = parse_type(rargs['name'], 'name', str)
    else:
        abort(make_response(jsonify(message = 'Argument "name" cannot be blank'), 400))

    if 'password' in rargs: 
        args['password'] = parse_type(rargs['password'], 'password', str)
    else:
        abort(make_response(jsonify(message = 'Argument "password" cannot be blank'), 400))

    if 'roles' in rargs: 
        args['roles'] = parse_roles(rargs['roles'])
    else:
        args['roles'] = []

    if 'username' in rargs:
        if UserTable.query.get(parse_type(rargs['username'], 'username', str)):
            abort(make_response(jsonify(message = 'User "{}" already exists'.format(username)), 409))
        args['username'] = rargs['username']
    else:
        abort(make_response(jsonify(message = 'Argument "username" cannot be blank'), 400))

    return args

