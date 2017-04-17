#!/usr/bin/env python3
""" Authentication Authorization Accounting """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

import hashlib
from flask import abort
from controller import api_key, cache
from controller.catalog.models import UserTable

def checkAuth(request):
    if request.args.get('api_key') and request.args.get('api_key') == api_key:
        # Correct API KEY: authenticated and authorized as admin user
        return {
            'username': 'admin',
            'roles': {
                'admin': {
                    'access_to': '*',
                    'can_write': True
                }
            }
        }
    elif request.args.get('api_key'):
        # Wrong API KEY: not authenticated
        abort(401)
    else:
        # User Authentication
        try:
            username = request.authorization.username
            password = hashlib.sha256(request.authorization.password.encode('utf-8')).hexdigest()
        except:
            abort(401)

    cached_user = cache.get(username)
    if cached_user:
        # User found in cache
        if cached_user['password'] == password:
            return cached_user
        abort(401)
    else:
        # User not found in cache
        user = UserTable.query.get_or_404(username)
        if user.password == password:
            # User authenticated, caching the user
            roles = {}
            for role in user.roles:
                roles[role.role] = {
                    'access_to': role.access_to,
                    'can_write': role.can_write
                }
            user = {
                'username': username,
                'password': user.password,
                'roles': roles
            }
            cache.set(username, user)
            return user
        else:
            # Wrong password
            abort(401)

def checkAuthz(request, roles = []):
    # User Authentication
    user = checkAuth(request)
    if len(roles) == 0:
        # No role required
        return user['username']
    for role in roles:
        if role in user['roles']:
            # A user role match the required one
            return user['username']
    # User does not have any required role
    abort(403)

def checkAuthzPath(request, path, would_write = False):
    import re
    # User Authentication
    user = checkAuth(request)

    user = User.query.get(username)
    if not user:
        return False
    for role in user.roles:
        try:
            pattern = re.compile(role.access_to)
            if pattern.match(path) != None:
                if would_write and not role.can_write:
                    return False
                return True
        except Exception as err:
            return False
    return False
