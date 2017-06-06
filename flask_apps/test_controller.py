#!/usr/bin/env python3.5
""" Tests for controller app """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import base64, getopt, json, logging, random, requests, sys, urllib3
urllib3.disable_warnings()

role_1 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(7))
role_2 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(7))
role_3 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(7))
username_1 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(9))
password_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
username_2 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(9))
password_2 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
password_3 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))

def usage():
    print('Usage: {} [OPTIONS]'.format(sys.argv[0]))
    print('')
    print('Options:')
    print('    -d             enable debug')
    print('    -c controller  the IP or domain name of the controller host')
    print('    -k key         API key')
    print('    -p password    a privileged password')
    print('    -u username    a privileged username')
    sys.exit(255)

def make_request(url, method = 'GET', data = None, username = None, password = None, api_key = None, expected_code = 200):
    basic_auth = None

    if api_key != None:
        logging.debug('Using API authentication')
        url = url + '?api_key={}'.format(api_key)
    elif username != None and password != None:
        logging.debug('Using basic authentication')
        basic_auth = requests.auth.HTTPBasicAuth(username, password)

    if method == 'GET':
        r = requests.get(url, verify = False, auth = basic_auth)
    elif method == 'POST':
        r = requests.post(url, verify = False, auth = basic_auth, json = data)
    elif method == 'PATCH':
        r = requests.patch(url, verify = False, auth = basic_auth, json = data)
    elif method == 'DELETE':
        r = requests.delete(url, verify = False, auth = basic_auth)
    else:
        logging.error('Method not supported')
        sys.exit(1)

    if r.status_code != expected_code:
        logging.error('Received {}, expecting {}'.format(r.status_code, expected_code))
        logging.error('Status is {}'.format(r.status_code))
        logging.error('Reason is {}'.format(r.reason))
        logging.error('Received content is {}'.format(r.text))
        sys.exit(1)

    try:
        returned_data = r.json()
    except:
        logging.error('Invalid JSON answer')
        logging.error('Status is {}'.format(r.status_code))
        logging.error('Reason is {}'.format(r.reason))
        logging.error('Content is {}'.format(r.text))
        sys.exit(1)

    logging.debug('Status is {}'.format(r.status_code))
    logging.debug('Reason is {}'.format(r.reason))
    logging.debug('Content is {}'.format(r.text))
    return returned_data

def main():
    level = logging.INFO
    admin_username = None
    admin_password = None
    api_key = None
    controller = None

    # Reading options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dc:u:p:k:')
    except getopt.GetoptError as err:
        sys.stderr.write('ERROR: {}\n'.format(err))
        usage()
        sys.exit(255)
    for opt, arg in opts:
        if opt == '-d':
            level = logging.DEBUG
        elif opt == '-c':
            controller = arg
        elif opt == '-u':
            admin_username = arg
        elif opt == '-p':
            admin_password = arg
        elif opt == '-k':
            api_key = arg
        else:
            assert False, 'unhandled option'

    # Checking options
    logging.basicConfig(level = level)
    if controller == None:
        logging.error('controller not set')
        sys.exit(255)
    if admin_username == None:
        logging.error('admin username not set')
        sys.exit(255)
    if admin_password == None:
        logging.error('admin password not set')
        sys.exit(255)
    if api_key == None:
        logging.error('API key not set')
        sys.exit(255)

    # /auth
    logging.info('Auth: unauthenticated request')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', expected_code = 401)

    logging.info('Auth: authentication via API')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', api_key = api_key, expected_code = 200)

    logging.info('Auth: basic authentication')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', username = admin_username, password = admin_password, expected_code = 200)

    # /roles
    logging.info('Roles: get all roles')
    returned_data = make_request('https://{}/api/v1/roles'.format(controller), method = 'GET', api_key = api_key, expected_code = 200)

    logging.info('Roles: get admin role')
    returned_data = make_request('https://{}/api/v1/roles/admin'.format(controller), method = 'GET', api_key = api_key, expected_code = 200)

    logging.info('Roles: adding role')
    data = {
        'role': role_1,
        'can_write': False,
        'access_to': '.*'
    }
    returned_data = make_request('https://{}/api/v1/roles'.format(controller), method = 'POST', data = data, api_key = api_key, expected_code = 200)
    if returned_data['data']['role'] != data['role']: sys.exit('role not validated')
    if returned_data['data']['access_to'] != data['access_to']: sys.exit('access_to not validated')
    if returned_data['data']['can_write'] != data['can_write']: sys.exit('can_write not validated')

    logging.info('Roles: get created role')
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_1), method = 'GET', api_key = api_key, expected_code = 200)
    if returned_data['data'][role_1]['role'] != role_1: sys.exit('role not validated')
    if returned_data['data'][role_1]['access_to'] != data['access_to']: sys.exit('access_to not validated')
    if returned_data['data'][role_1]['can_write'] != data['can_write']: sys.exit('can_write not validated')

    logging.info('Roles: try to create a minimal role')
    data = {
        'role': role_2
    }
    returned_data = make_request('https://{}/api/v1/roles'.format(controller), method = 'POST', data = data, api_key = api_key, expected_code = 200)
    if returned_data['data']['role'] != data['role']: sys.exit('role not validated')
    if returned_data['data']['access_to'] != None: sys.exit('access_to not validated')
    if returned_data['data']['can_write'] != None: sys.exit('can_write not validated')

    logging.info('Roles: edit role')
    data = {
        'can_write': True,
        'access_to': 'something.*'
    }
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_2), method = 'PATCH', data = data, api_key = api_key, expected_code = 200)
    if returned_data['data']['role'] != role_2: sys.exit('role not validated')
    if returned_data['data']['access_to'] != data['access_to']: sys.exit('access_to not validated')
    if returned_data['data']['can_write'] != data['can_write']: sys.exit('can_write not validated')

    logging.info('Roles: get modified role')
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_2), method = 'GET', api_key = api_key, expected_code = 200)
    if returned_data['data'][role_2]['role'] != role_2: sys.exit('role not validated')
    if returned_data['data'][role_2]['access_to'] != data['access_to']: sys.exit('access_to not validated')
    if returned_data['data'][role_2]['can_write'] != data['can_write']: sys.exit('can_write not validated')

    logging.info('Roles: try to create a fake role')
    data = {}
    returned_data = make_request('https://{}/api/v1/roles'.format(controller), method = 'POST', data = data, api_key = api_key, expected_code = 400)

    # /users
    logging.info('Users: get all users')
    returned_data = make_request('https://{}/api/v1/users'.format(controller), method = 'GET', api_key = api_key, expected_code = 200)

    logging.info('Users: get admin user')
    returned_data = make_request('https://{}/api/v1/users/admin'.format(controller), method = 'GET', api_key = api_key, expected_code = 200)

    logging.info('Users: adding user')
    data = {
        'email': '{}@example.com'.format(username_1),
        'labels': 100,
        'name': 'User 1',
        'password': password_1,
        'roles': [role_1],
        'username': username_1
    }
    returned_data = make_request('https://{}/api/v1/users'.format(controller), method = 'POST', data = data, api_key = api_key, expected_code = 200)
    if returned_data['data']['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data']['labels'] != data['labels']: sys.exit('labels not validated')
    if returned_data['data']['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data']['roles'] != data['roles']: sys.exit('roles not validated')
    if returned_data['data']['username'] != data['username']: sys.exit('username not validated')

    logging.info('Users: get created user')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_1), method = 'GET', api_key = api_key, expected_code = 200)
    if returned_data['data'][username_1]['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data'][username_1]['labels'] != data['labels']: sys.exit('labels not validated')
    if returned_data['data'][username_1]['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data'][username_1]['roles'] != data['roles']: sys.exit('roles not validated')
    if returned_data['data'][username_1]['username'] != data['username']: sys.exit('username not validated')

    logging.info('Users: basic authentication')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', username = username_1, password = password_1, expected_code = 200)

    logging.info('Users: adding a tiny user')
    data = {
        'email': '{}@example.com'.format(username_2),
        'name': 'User 1',
        'password': password_2,
        'username': username_2
    }
    returned_data = make_request('https://{}/api/v1/users'.format(controller), method = 'POST', data = data, api_key = api_key, expected_code = 200)
    if returned_data['data']['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data']['labels'] != 0: sys.exit('labels not validated')
    if returned_data['data']['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data']['roles'] != []: sys.exit('roles not validated')
    if returned_data['data']['username'] != data['username']: sys.exit('username not validated')

    logging.info('Users: get created user')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'GET', api_key = api_key, expected_code = 200)
    if returned_data['data'][username_2]['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data'][username_2]['labels'] != 0: sys.exit('labels not validated')
    if returned_data['data'][username_2]['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data'][username_2]['roles'] != []: sys.exit('roles not validated')
    if returned_data['data'][username_2]['username'] != data['username']: sys.exit('username not validated')

    logging.info('Users: edit user')
    data = {
        'email': '{}@example.net'.format(username_2),
        'labels': 111,
        'name': 'Mr User 1',
        'password': password_3,
        'roles': [role_1, role_2, 'admin']
    }
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'PATCH', data = data, api_key = api_key, expected_code = 200)
    if returned_data['data']['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data']['labels'] != 111: sys.exit('labels not validated')
    if returned_data['data']['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data']['roles'] != [role_1, role_2, 'admin']: sys.exit('roles not validated')
    if returned_data['data']['username'] != username_2: sys.exit('username not validated')

    logging.info('Users: get modified user')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'GET', api_key = api_key, expected_code = 200)
    if returned_data['data'][username_2]['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data'][username_2]['labels'] != data['labels']: sys.exit('labels not validated')
    if returned_data['data'][username_2]['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data'][username_2]['roles'] != data['roles']: sys.exit('roles not validated')
    if returned_data['data'][username_2]['username'] != username_2: sys.exit('username not validated')

    logging.info('Users: basic authentication')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', username = username_2, password = password_3, expected_code = 200)

    logging.info('Users: set a wrong user')
    data = {
        'email': '{}@example.net'.format(username_2),
        'roles': [role_1, role_3, 'admin']
    }
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'PATCH', data = data, api_key = api_key, expected_code = 400)

    # Cleaning

    logging.info('Roles: delete role')
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_1), method = 'DELETE', api_key = api_key, expected_code = 200)

    logging.info('Roles: delete role')
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_2), method = 'DELETE', api_key = api_key, expected_code = 200)

    logging.info('Users: delete username')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_1), method = 'DELETE', api_key = api_key, expected_code = 200)

    logging.info('Users: delete username')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'DELETE', api_key = api_key, expected_code = 200)

if __name__ == '__main__':
    main()
