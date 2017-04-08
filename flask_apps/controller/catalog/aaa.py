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
        username = 'admin'
        password = UserTable.query.get('admin').password
    elif request.args.get('api_key'):
        # Wrong API KEY: not authenticated
        abort(401)
    else:
        # User Authentication
        username = request.authorization.username
        password = hashlib.sha256(request.authorization.password.encode('utf-8')).hexdigest()

    # Caching user
    if not cache.get(username):
        # User not found in cache
        user = UserTable.query.get(username)
        if not user:
            # User does not exist
            abort(404)
        cache.set(username, {
            'password': user.password,
            'roles': user.roles
        })

    # Checking user authentication
    user = cache.get(username)
    if user['password'] == password:
        return user
    abort(401)

def checkAuthz(request, roles):
    # User Authentication
    user = checkAuth(request)
    for role in user['roles']:
        if role.role in roles:
            # A user role match the required one
            return True
    abort(403)
