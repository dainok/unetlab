#!/usr/bin/env python3
""" Authentication Authorization Accounting """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from controller.catalog.models import UserTable

def checkAuth(username, password):
    user = UserTable.query.get(username)
    if not user:
        return False
    if user.password != hashlib.sha256(password.encode('utf-8')).hexdigest():
        return False
    return True

def checkAuthz(username, roles):
    auth = request.authorization
    user = UserTable.query.get(username)
    if not user:
        return False
    for role in user.roles:
        if role.role in roles:
            return True
    return False

def checkAuthzPath(username, path, would_write = False):
    import re
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

