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
router_1 = random.randint(1000, 10000)
router_2 = random.randint(1000, 10000)
username_1 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(9))
password_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
username_2 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(9))
password_2 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
password_3 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
repository_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
repository_username_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
repository_password_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
image = 'L3-ADVENTERPRISEK9-M-15.5-2T'
lab_1 = {
    'name': 'UNetLabv2 Test 1',
    'repository': 'local',
    'version': 1,
    'author': 'Andrea Dainese <andrea.dainese@gmail.com>',
    'topology': {
        'nodes': {
            '0': {
                'name': 'R1',
                'type': 'iol',
                'image': image,
                'iol_id': 1,
                'ethernet': 1,
                'serial': 0,
                'ram': 1024,
                'interfaces': {
                    '0': {
                        'name': 'e0/0',
                        'management': True
                    },
                    '16': {
                        'name': 'e0/1',
                        'connection': 0,
                    }
                }
            },
            '1': {
                'name': 'R2',
                'type': 'iol',
                'image': image,
                'iol_id': 2,
                'ethernet': 1,
                'serial': 0,
                'ram': 1024,
                'interfaces': {
                    '0': {
                        'name': 'e0/0',
                    },
                    '16': {
                        'name': 'e0/1',
                        'connection': 0,
                    }
                }
            }
        },
        'connections': {
            '0': {
                'type': 'ethernet',
            }
        }
    }
}


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

def make_request(url, method = 'GET', data = None, username = None, password = None, api_key = None, expected_codes = 200, is_json = True):
    basic_auth = None

    if api_key != None:
        logging.debug('Using API authentication')
        if '?' in url:
            url = url + '&api_key={}'.format(api_key)
        else:
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

    if isinstance(expected_codes, int):
        expected_codes = [expected_codes]
    found_expected_code = False
    for expected_code in expected_codes:
        if r.status_code == expected_code:
            found_expected_code = True
            break
    if not found_expected_code:
        logging.error('Received {}, expecting {}'.format(r.status_code, expected_codes))
        logging.error('Status is {}'.format(r.status_code))
        logging.error('Reason is {}'.format(r.reason))
        logging.error('Received content is {}'.format(r.text))
        sys.exit(1)

    if is_json:
        try:
            returned_data = r.json()
        except:
            logging.error('Invalid JSON answer')
            logging.error('Status is {}'.format(r.status_code))
            logging.error('Reason is {}'.format(r.reason))
            logging.error('Content is {}'.format(r.text))
            sys.exit(1)
    else:
        returned_data = r.text

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
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', expected_codes = 401)

    logging.info('Auth: authentication via API')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', api_key = api_key, expected_codes = 200)

    logging.info('Auth: basic authentication')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', username = admin_username, password = admin_password, expected_codes = 200)

    # /roles

    logging.info('Roles: get all roles')
    returned_data = make_request('https://{}/api/v1/roles'.format(controller), method = 'GET', api_key = api_key, expected_codes = 200)

    logging.info('Roles: get admin role')
    returned_data = make_request('https://{}/api/v1/roles/admin'.format(controller), method = 'GET', api_key = api_key, expected_codes = 200)

    logging.info('Roles: adding role')
    data = {
        'role': role_1,
        'can_write': False,
        'access_to': '.*'
    }
    returned_data = make_request('https://{}/api/v1/roles'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['role'] != data['role']: sys.exit('role not validated')
    if returned_data['data']['access_to'] != data['access_to']: sys.exit('access_to not validated')
    if returned_data['data']['can_write'] != data['can_write']: sys.exit('can_write not validated')

    logging.info('Roles: get created role')
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_1), method = 'GET', api_key = api_key, expected_codes = 200)
    if returned_data['data'][role_1]['role'] != role_1: sys.exit('role not validated')
    if returned_data['data'][role_1]['access_to'] != data['access_to']: sys.exit('access_to not validated')
    if returned_data['data'][role_1]['can_write'] != data['can_write']: sys.exit('can_write not validated')

    logging.info('Roles: try to create a minimal role')
    data = {
        'role': role_2
    }
    returned_data = make_request('https://{}/api/v1/roles'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['role'] != data['role']: sys.exit('role not validated')
    if returned_data['data']['access_to'] != None: sys.exit('access_to not validated')
    if returned_data['data']['can_write'] != None: sys.exit('can_write not validated')

    logging.info('Roles: edit role')
    data = {
        'can_write': True,
        'access_to': 'something.*'
    }
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_2), method = 'PATCH', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['role'] != role_2: sys.exit('role not validated')
    if returned_data['data']['access_to'] != data['access_to']: sys.exit('access_to not validated')
    if returned_data['data']['can_write'] != data['can_write']: sys.exit('can_write not validated')

    logging.info('Roles: get modified role')
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_2), method = 'GET', api_key = api_key, expected_codes = 200)
    if returned_data['data'][role_2]['role'] != role_2: sys.exit('role not validated')
    if returned_data['data'][role_2]['access_to'] != data['access_to']: sys.exit('access_to not validated')
    if returned_data['data'][role_2]['can_write'] != data['can_write']: sys.exit('can_write not validated')

    logging.info('Roles: try to create a fake role')
    data = {}
    returned_data = make_request('https://{}/api/v1/roles'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 400)

    # /users

    logging.info('Users: get all users')
    returned_data = make_request('https://{}/api/v1/users'.format(controller), method = 'GET', api_key = api_key, expected_codes = 200)

    logging.info('Users: get admin user')
    returned_data = make_request('https://{}/api/v1/users/admin'.format(controller), method = 'GET', api_key = api_key, expected_codes = 200)

    logging.info('Users: adding user')
    data = {
        'email': '{}@example.com'.format(username_1),
        'labels': 100,
        'name': 'User 1',
        'password': password_1,
        'roles': [role_1],
        'username': username_1
    }
    returned_data = make_request('https://{}/api/v1/users'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data']['labels'] != data['labels']: sys.exit('labels not validated')
    if returned_data['data']['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data']['roles'] != data['roles']: sys.exit('roles not validated')
    if returned_data['data']['username'] != data['username']: sys.exit('username not validated')

    logging.info('Users: get created user')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_1), method = 'GET', api_key = api_key, expected_codes = 200)
    if returned_data['data'][username_1]['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data'][username_1]['labels'] != data['labels']: sys.exit('labels not validated')
    if returned_data['data'][username_1]['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data'][username_1]['roles'] != data['roles']: sys.exit('roles not validated')
    if returned_data['data'][username_1]['username'] != data['username']: sys.exit('username not validated')

    logging.info('Users: basic authentication')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', username = username_1, password = password_1, expected_codes = 200)

    logging.info('Users: adding a tiny user')
    data = {
        'email': '{}@example.com'.format(username_2),
        'name': 'User 1',
        'password': password_2,
        'username': username_2
    }
    returned_data = make_request('https://{}/api/v1/users'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data']['labels'] != 0: sys.exit('labels not validated')
    if returned_data['data']['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data']['roles'] != []: sys.exit('roles not validated')
    if returned_data['data']['username'] != data['username']: sys.exit('username not validated')

    logging.info('Users: get created user')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'GET', api_key = api_key, expected_codes = 200)
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
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'PATCH', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data']['labels'] != 111: sys.exit('labels not validated')
    if returned_data['data']['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data']['roles'] != [role_1, role_2, 'admin']: sys.exit('roles not validated')
    if returned_data['data']['username'] != username_2: sys.exit('username not validated')

    logging.info('Users: get modified user')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'GET', api_key = api_key, expected_codes = 200)
    if returned_data['data'][username_2]['email'] != data['email']: sys.exit('email not validated')
    if returned_data['data'][username_2]['labels'] != data['labels']: sys.exit('labels not validated')
    if returned_data['data'][username_2]['name'] != data['name']: sys.exit('name not validated')
    if returned_data['data'][username_2]['roles'] != data['roles']: sys.exit('roles not validated')
    if returned_data['data'][username_2]['username'] != username_2: sys.exit('username not validated')

    logging.info('Users: basic authentication')
    returned_data = make_request('https://{}/api/v1/auth'.format(controller), method = 'GET', username = username_2, password = password_3, expected_codes = 200)

    logging.info('Users: set a wrong user')
    data = {
        'email': '{}@example.net'.format(username_2),
        'roles': [role_1, role_3, 'admin']
    }
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'PATCH', data = data, api_key = api_key, expected_codes = 400)

    # /routers

    logging.info('Routers: adding a router')
    data = {
        'id': router_1,
        'inside_ip': '172.31.0.3/16',
        'outside_ip': '1.1.1.131/24'
    }
    returned_data = make_request('https://{}/api/v1/routers'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['id'] != data['id']: sys.exit('id not validated')
    if returned_data['data']['inside_ip'] != data['inside_ip']: sys.exit('inside_ip not validated')
    if returned_data['data']['outside_ip'] != data['outside_ip']: sys.exit('outside_ip not validated')

    logging.info('Routers: get created router')
    returned_data = make_request('https://{}/api/v1/routers/{}'.format(controller, router_1), method = 'GET', api_key = api_key, expected_codes = 200)
    if returned_data['data'][str(router_1)]['id'] != data['id']: sys.exit('id not validated')
    if returned_data['data'][str(router_1)]['inside_ip'] != data['inside_ip']: sys.exit('inside_ip not validated')
    if returned_data['data'][str(router_1)]['outside_ip'] != data['outside_ip']: sys.exit('outside_ip not validated')

    logging.info('Routers: register a new router')
    data = {
        'id': router_2,
        'inside_ip': '172.32.0.3/16'
    }
    returned_data = make_request('https://{}/api/v1/routers'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['id'] != data['id']: sys.exit('id not validated')
    if returned_data['data']['inside_ip'] != data['inside_ip']: sys.exit('inside_ip not validated')

    logging.info('Routers: get registered router')
    returned_data = make_request('https://{}/api/v1/routers/{}'.format(controller, router_2), method = 'GET', api_key = api_key, expected_codes = 200)
    if returned_data['data'][str(router_2)]['id'] != data['id']: sys.exit('id not validated')
    if returned_data['data'][str(router_2)]['inside_ip'] != data['inside_ip']: sys.exit('inside_ip not validated')
    if returned_data['data'][str(router_2)]['outside_ip'] != None: sys.exit('outside_ip not validated')

    logging.info('Routers: register an existent router')
    data = {
        'id': router_1,
        'inside_ip': '172.31.0.3/16'
    }
    returned_data = make_request('https://{}/api/v1/routers'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['id'] != data['id']: sys.exit('id not validated')
    if returned_data['data']['inside_ip'] != data['inside_ip']: sys.exit('inside_ip not validated')

    logging.info('Routers: get registered router')
    returned_data = make_request('https://{}/api/v1/routers/{}'.format(controller, router_1), method = 'GET', api_key = api_key, expected_codes = 200)
    if returned_data['data'][str(router_1)]['id'] != data['id']: sys.exit('id not validated')
    if returned_data['data'][str(router_1)]['inside_ip'] != data['inside_ip']: sys.exit('inside_ip not validated')

    logging.info('Routers: edit router')
    data = {
        'inside_ip': '172.34.0.3/16',
        'outside_ip': '1.1.1.134/24'
    }
    returned_data = make_request('https://{}/api/v1/routers/{}'.format(controller, router_1), method = 'PATCH', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['inside_ip'] != data['inside_ip']: sys.exit('inside_ip not validated')
    if returned_data['data']['outside_ip'] != data['outside_ip']: sys.exit('outside_ip not validated')

    logging.info('Routers: get modified router')
    returned_data = make_request('https://{}/api/v1/routers/{}'.format(controller, router_1), method = 'GET', api_key = api_key, expected_codes = 200)
    if returned_data['data'][str(router_1)]['inside_ip'] != data['inside_ip']: sys.exit('inside_ip not validated')
    if returned_data['data'][str(router_1)]['outside_ip'] != data['outside_ip']: sys.exit('outside_ip not validated')

    logging.info('Routers: bootstrap router')
    returned_data = make_request('https://{}/api/v1/bootstrap/routers/{}'.format(controller, router_1), method = 'GET', api_key = api_key, expected_codes = 200, is_json = False)

    # /repositories

    logging.info('Repositories: adding a repository')
    data = {
        'repository': repository_1,
        'url': 'https://github.com/dainok/rrlabs'
    }
    returned_data = make_request('https://{}/api/v1/repositories'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    if 'task' not in returned_data: sys.exit('task not validated')
    task_repository_1 = returned_data['task']

    logging.info('Repositories: get created repository')
    returned_data = make_request('https://{}/api/v1/repositories/{}'.format(controller, repository_1), method = 'GET', api_key = api_key, expected_codes = [200, 404])

    logging.info('Repositories: edit repository')
    data = {
        'url': 'https://github.com/dainok/labs',
        'username': repository_username_1,
        'password': repository_password_1
    }
    returned_data = make_request('https://{}/api/v1/repositories/{}'.format(controller, 'local'), method = 'PATCH', data = data, api_key = api_key, expected_codes = 200)
    if returned_data['data']['id'] != 'local': sys.exit('id not validated')
    if returned_data['data']['url'] != data['url']: sys.exit('url not validated')
    if returned_data['data']['username'] != data['username']: sys.exit('username not validated')

    logging.info('Repositories: get modidied repository')
    returned_data = make_request('https://{}/api/v1/repositories/{}'.format(controller, 'local'), method = 'GET', api_key = api_key, expected_codes = [200])
    if returned_data['data']['local']['id'] != 'local': sys.exit('id not validated')
    if returned_data['data']['local']['url'] != data['url']: sys.exit('url not validated')
    if returned_data['data']['local']['username'] != data['username']: sys.exit('username not validated')

    # /labs

    logging.info('Labs: adding a lab')
    data = lab_1
    returned_data = make_request('https://{}/api/v1/labs'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    lab_id_1 = returned_data['data']['id']

    logging.info('Labs: get created lab')
    returned_data = make_request('https://{}/api/v1/labs/{}'.format(controller, lab_id_1), method = 'GET', api_key = api_key, expected_codes = [200])

    logging.info('Labs: adding a lab with commit')
    data = lab_1
    returned_data = make_request('https://{}/api/v1/labs?commit=true'.format(controller), method = 'POST', data = data, api_key = api_key, expected_codes = 200)
    lab_id_2 = returned_data['data']['id']

    logging.info('Labs: get created lab')
    returned_data = make_request('https://{}/api/v1/labs/{}'.format(controller, lab_id_2), method = 'GET', api_key = api_key, expected_codes = [200])


    # patch
    # get

    # patch with commit
    # get


    #api.add_resource(Lab, '/api/v1/labs', '/api/v1/labs/<string:lab_id>')
    #api.add_resource(BootstrapNode, '/api/v1/bootstrap/nodes/<string:label>')
    #api.add_resource(Routing, '/api/v1/routing')
    #api.add_resource(Task, '/api/v1/tasks', '/api/v1/tasks/<string:task_id>')

    # /static

    logging.info('Static: get wrapper_dynamips.py')
    returned_data = make_request('https://{}/static/node/wrapper_dynamips.py'.format(controller), method = 'GET', expected_codes = 200, is_json = False)

    logging.info('Static: get wrapper_iol.py')
    returned_data = make_request('https://{}/static/node/wrapper_iol.py'.format(controller), method = 'GET', expected_codes = 200, is_json = False)

    logging.info('Static: get wrapper_qemu.py')
    returned_data = make_request('https://{}/static/node/wrapper_qemu.py'.format(controller), method = 'GET', expected_codes = 200, is_json = False)

    logging.info('Static: get router.py')
    returned_data = make_request('https://{}/static/router/router.py'.format(controller), method = 'GET', expected_codes = 200, is_json = False)

    logging.info('Static: get router_modules.py')
    returned_data = make_request('https://{}/static/router/router_modules.py'.format(controller), method = 'GET', expected_codes = 200, is_json = False)

    # Cleaning

    logging.info('Roles: delete role')
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_1), method = 'DELETE', api_key = api_key, expected_codes = 200)

    logging.info('Roles: delete role')
    returned_data = make_request('https://{}/api/v1/roles/{}'.format(controller, role_2), method = 'DELETE', api_key = api_key, expected_codes = 200)

    logging.info('Routers: delete router')
    returned_data = make_request('https://{}/api/v1/routers/{}'.format(controller, router_1), method = 'DELETE', api_key = api_key, expected_codes = 200)

    logging.info('Routers: delete router')
    returned_data = make_request('https://{}/api/v1/routers/{}'.format(controller, router_2), method = 'DELETE', api_key = api_key, expected_codes = 200)

    logging.info('Users: delete username')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_1), method = 'DELETE', api_key = api_key, expected_codes = 200)

    logging.info('Users: delete username')
    returned_data = make_request('https://{}/api/v1/users/{}'.format(controller, username_2), method = 'DELETE', api_key = api_key, expected_codes = 200)

    logging.info('Repositories: delete repository')
    returned_data = make_request('https://{}/api/v1/repositories/{}'.format(controller, repository_1), method = 'DELETE', api_key = api_key, expected_codes = [200, 404])

    logging.info('Labs: delete lab')
    returned_data = make_request('https://{}/api/v1/labs/{}'.format(controller, lab_id_1), method = 'DELETE', api_key = api_key, expected_codes = 200)

    logging.info('Labs: delete lab')
    returned_data = make_request('https://{}/api/v1/labs/{}'.format(controller, lab_id_2), method = 'DELETE', api_key = api_key, expected_codes = 200)

if __name__ == '__main__':
    main()
