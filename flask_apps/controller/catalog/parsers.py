#!/usr/bin/env python3
""" Data parsers """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

import os
from flask_restful import reqparse
from controller import config
from controller.catalog.models import RoleTable

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
            if 'interfaces' in node:
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

add_role_parser = reqparse.RequestParser()
add_role_parser.add_argument('role', type = str, required = True, location = 'json', help = 'role cannot be blank')
add_role_parser.add_argument('can_write', type = bool, required = False, location = 'json', help = 'can_write must be boolean')
add_role_parser.add_argument('access_to', type = str, required = False, location = 'json', help = 'access_to must be a regex')

patch_role_parser = reqparse.RequestParser()
patch_role_parser.add_argument('can_write', type = bool, required = False, store_missing = False, location = 'json', help = 'can_write must be boolean')
patch_role_parser.add_argument('access_to', type = str, required = False, store_missing = False, location = 'json', help = 'access_to must be a regex')

add_user_parser = reqparse.RequestParser()
add_user_parser.add_argument('username', type = str, required = True, location = 'json', help = 'username cannot be blank')
add_user_parser.add_argument('password', type = str, required = True, location = 'json', help = 'password cannot be blank')
add_user_parser.add_argument('name', type = str, required = True, location = 'json', help = 'name cannot be blank')
add_user_parser.add_argument('email', type = str, required = True, location = 'json', help = 'email cannot be blank')
add_user_parser.add_argument('labels', type = type_label, required = False, location = 'json', help = 'labels must be integer and greater than -1')
add_user_parser.add_argument('roles', type = type_roles, required = False, location = 'json', help = 'roles must be a list of valid roles')

patch_user_parser = reqparse.RequestParser()
patch_user_parser.add_argument('password', type = str, required = False, store_missing = False, location = 'json', help = 'password cannot be blank')
patch_user_parser.add_argument('name', type = str, required = False, store_missing = False, location = 'json', help = 'name cannot be blank')
patch_user_parser.add_argument('email', type = str, required = False, store_missing = False, location = 'json', help = 'email cannot be blank')
patch_user_parser.add_argument('labels', type = type_label, required = False, store_missing = False, location = 'json', help = 'labels must be integer and greater than -1')
patch_user_parser.add_argument('roles', type = type_roles, required = False, store_missing = False, location = 'json', help = 'roles must be a list of valid roles')
