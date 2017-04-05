#!/usr/bin/env python3
""" Data parsers """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from flask_restful import reqparse

def type_label(arg):
    try:
        label = int(arg)
    except:
        raise ValueError

    if label >= -1:
        return label
    else:
        raise ValueError

def type_roles(arg):
    if type(arg) is list:
        print(arg)
        for role in arg:
            print(role)
            print(Role.query.get(role))
        return arg
    else:
        raise ValueError


user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type = str, required = True, location = 'json', help = 'username cannot be blank')
user_parser.add_argument('password', type = str, required = True, location = 'json', help = 'password cannot be blank')
user_parser.add_argument('name', type = str, required = True, location = 'json', help = 'name cannot be blank')
user_parser.add_argument('email', type = str, required = True, location = 'json', help = 'email cannot be blank')
user_parser.add_argument('labels', type = type_label, required = False, location = 'json', help = 'labels must be integer and greater than -1')
user_parser.add_argument('roles', type = type_roles, required = False, location = 'json', help = 'roles must be a list of valid roles')

