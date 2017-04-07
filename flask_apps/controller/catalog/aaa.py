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

def checkAuth(username, password):
    if cache.get(username):
        user = cache.get(username)
    else:
        user = UserTable.query.get(username)
    if user and user.password == hashlib.sha256(password.encode('utf-8')).hexdigest():
        cache.set(username, user)
        return user
    abort(401)

def checkAuthz(request, roles):
    if request.args.get('api_key') == api_key:
        # Correct API KEY: authenticated and authorized
        return True
    elif request.args.get('api_key'):
        # Wrong API KEY: not authenticated
        abort(401)
    else:
        # User Authentication
        user = checkAuth(request.authorization.username, request.authorization.password)
        print(user)
        print(user.roles)
    for role in user.roles:
        if role.role in roles:
            # A user role match the required one
            return True
    abort(403)
