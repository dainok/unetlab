#!/usr/bin/env python3
""" Data parsers """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import ipaddress, os, validate_email
from flask import abort, jsonify, make_response, request
from flask_restful import reqparse
from controller import config
from controller.catalog.models import RoleTable, UserTable

def parse_email(email):
    email = parse_type(email, 'email', str)
    if not validate_email.validate_email(email):
        abort(make_response(jsonify(message = 'Argument "email" is not valid'), 400))
    return email

def parse_json():
    try:
        rargs = request.json
    except:
        abort(make_response(jsonify(message = 'Input data is not a valid JSON'), 400))
    return rargs

def parse_labels(labels):
    # A label must be integer greater than -1
    labels = parse_type(labels, 'labels', int)
    if labels < 0:
        abort(make_response(jsonify(message = 'Argument "labels" must be equal or greater than 0'), 400))
    return labels

def parse_password(password):
    password = parse_type(password, 'password', str)
    if password == '':
        abort(make_response(jsonify(message = 'Argument "password" cannot be empty'), 400))
    return password

def parse_roles(roles):
    roles = parse_type(roles, 'roles', list)
    for role in roles:
        if not RoleTable.query.get(role):
            abort(make_response(jsonify(message = 'Role "{}" not found'.format(role)), 400))
    return roles

def parse_type(arg, arg_name, arg_type):
    if not isinstance(arg, arg_type):
        abort(make_response(jsonify(message = 'Argument "{}" must be "{}"'.format(arg_name, arg_type)), 400))
    return arg

def auth_parser_patch(username):
    args = {}
    rargs = parse_json()

    if not UserTable.query.get(parse_type(username, 'username', str)):
        abort(make_response(jsonify(message = 'Username "{}" not found'.format(username)), 404))

    if 'password' in rargs: 
        args['password'] = parse_password(rargs['password'])
    else:
        abort(make_response(jsonify(message = 'Argument "password " is not valid'), 400))

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
            abort(make_response(jsonify(message = 'Role "{}" already exists'.format(role)), 409))
        args['role'] = rargs['role']
    else:
        abort(make_response(jsonify(message = 'Argument "role" cannot be blank'), 400))

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






# TODO convert to custom parse

def type_ipinterface(arg):
    try:
        return ipaddress.IPv4Interface(arg)
    except:
        raise ValueError
    raise ValueError

def type_label(arg):
    # A label must be integer greater than -1
    try:
        label = int(arg)
    except:
        raise ValueError

    if label >= -1:
        return label
    raise ValueError

def type_repository(arg):
    # A repository must exist under lab_repository
    if os.path.isdir('{}/{}'.format(config['app']['lab_repository'], arg)):
        return arg
    raise ValueError

def type_roles(arg):
    # A role must be defined in RoleTable
    if type(arg) is list:
        for role in arg:
            if not RoleTable.query.get(role):
                raise ValueError
        return arg
    raise ValueError

def type_topology(arg):
    # Topology is a dict
    if not isinstance(arg, dict):
        raise ValueError
    # Topology can have nodes and connections
    if 'nodes' in arg:
        # nodes is a dict
        if not isinstance(arg['nodes'], dict):
            raise ValueError
        for node_id, node in arg['nodes'].items():
            # node_id is numeric
            if not node_id.isdigit():
                raise ValueError
            # node is a dict
            if not isinstance(node, dict):
                raise ValueError
            # node can have interfaces
            if 'interfaces' in node.items():
                # interfaces is a dict
                if not isinstance(node['interfaces'], dict):
                    raise ValueError
                for interface_id, interface in node['interfaces'].items():
                    # interface_id is numeric
                    if not interface_id.isdigit():
                        raise ValueError
                    # interface is a dict
                    if not instance(interface, dict):
                        raise ValueError
    if 'connections' in arg:
        # connections is a dict
        if not isinstance(arg['connections'], dict):
            raise ValueError
        for connection_id, connection in arg['connections'].items():
            # connection_id is numeric
            if not connection_id.isdigit():
                raise ValueError
            # connection is a dict
            if not isinstance(connection, dict):
                raise ValueError
    return arg

add_lab_parser = reqparse.RequestParser()
add_lab_parser.add_argument('commit', type = bool, required = False, help = 'commit must be boolean')
add_lab_parser.add_argument('name', type = str, required = True, location = 'json', help = 'name cannot be blank')
add_lab_parser.add_argument('repository', type = type_repository, required = True, location = 'json', help = 'repository must be present')
add_lab_parser.add_argument('author', type = str, required = False, location = 'json', help = 'author must be a string')
add_lab_parser.add_argument('version', type = int, required = False, location = 'json', help = 'version must be a string')
add_lab_parser.add_argument('topology', type = type_topology, required = False, location = 'json', help = 'topology must be valid')

delete_lab_parser = reqparse.RequestParser()
delete_lab_parser.add_argument('commit', type = bool, required = False, help = 'commit must be boolean')

add_repository_parser = reqparse.RequestParser()
add_repository_parser.add_argument('repository', type = str, required = True, location = 'json', help = 'repository cannot be blank')
add_repository_parser.add_argument('url', type = str, required = True, location = 'json', help = 'url cannot be blank')
add_repository_parser.add_argument('username', type = str, required = False, location = 'json', help = 'username must be a string')
add_repository_parser.add_argument('password', type = str, required = False, location = 'json', help = 'password must be a string')

patch_repository_parser = reqparse.RequestParser()
patch_repository_parser.add_argument('url', type = str, required = True, location = 'json', help = 'url cannot be blank')
patch_repository_parser.add_argument('username', type = str, required = False, location = 'json', help = 'username must be a string')
patch_repository_parser.add_argument('password', type = str, required = False, location = 'json', help = 'password must be a string')

add_router_parser = reqparse.RequestParser()
add_router_parser.add_argument('id', type = type_label, required = True, location = 'json', help = 'id must be integer and greater than -1')
add_router_parser.add_argument('inside_ip', type = type_ipinterface, required = True, location = 'json', help = 'inside_ip must be a valid IP address')
add_router_parser.add_argument('outside_ip', type = type_ipinterface, required = False, location = 'json', help = 'outside_ip must be a valid IP address')

patch_router_parser = reqparse.RequestParser()
patch_router_parser.add_argument('inside_ip', type = type_ipinterface, required = True, location = 'json', help = 'inside_ip must be a valid IP address')
patch_router_parser.add_argument('outside_ip', type = type_ipinterface, required = False, location = 'json', help = 'outside_ip must be a valid IP address')

