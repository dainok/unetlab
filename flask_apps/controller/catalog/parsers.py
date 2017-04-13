#!/usr/bin/env python3
""" Data parsers """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from flask_restful import reqparse
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

def type_roles(arg):
    # A role must be defined in RoleTable
    if type(arg) is list:
        for role in arg:
            if RoleTable.query.get(role):
                return arg
    raise ValueError

add_role_parser = reqparse.RequestParser()
add_role_parser.add_argument('role', type = str, required = True, location = 'json', help = 'role cannot be blank')
add_role_parser.add_argument('can_write', type = bool, required = False, location = 'json', help = 'can_write must be boolean')
add_role_parser.add_argument('access_to', type = str, required = False, location = 'json')

add_user_parser = reqparse.RequestParser()
add_user_parser.add_argument('username', type = str, required = True, location = 'json', help = 'username cannot be blank')
add_user_parser.add_argument('password', type = str, required = True, location = 'json', help = 'password cannot be blank')
add_user_parser.add_argument('name', type = str, required = True, location = 'json', help = 'name cannot be blank')
add_user_parser.add_argument('email', type = str, required = True, location = 'json', help = 'email cannot be blank')
add_user_parser.add_argument('labels', type = type_label, required = False, location = 'json', help = 'labels must be integer and greater than -1')
add_user_parser.add_argument('roles', type = type_roles, required = False, location = 'json', help = 'roles must be a list of valid roles')

