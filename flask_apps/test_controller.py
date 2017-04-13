#!/usr/bin/env python3
""" Tests for controller app """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from controller import app, api_key
import base64, json, os, random, tempfile, unittest

admin_username = 'admin'
admin_password = 'admin'

headers = {
    'Authorization': 'Basic ' + base64.b64encode(str.encode(admin_username) + b':' + str.encode(admin_password)).decode('utf-8'),
}

role_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(8))
role_2 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(8))
username_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(10))
password_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
username_2 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(10))
password_2 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_001_get_roles_via_api(self):
        # curl -s -D- -X GET http://127.0.0.1:5000/api/v1/roles?api_key=zqg81ge585t0bt3qe0sjj1idvw7hv7vfgc11dsq6
        url = '/api/v1/roles?api_key={}'.format(api_key)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_002_get_roles_via_auth(self):
        # curl -s -D- -u admin:admin -X GET http://127.0.0.1:5000/api/v1/roles
        url = '/api/v1/roles'
        response = self.app.get(url, headers = headers)
        self.assertEqual(response.status_code, 200)

    def test_003_post_role_via_api(self):
        # curl -s -D- -X POST -d '{"role":"test1","can_write":true,"access_to":"*"}' -H 'Content-type: application/json' http://127.0.0.1:5000/api/v1/roles?api_key=zqg81ge585t0bt3qe0sjj1idvw7hv7vfgc11dsq6
        url = '/api/v1/roles?api_key={}'.format(api_key)
        data = {
            'role': role_1,
            'can_write': True,
            'access_to': '*'
        }
        response = self.app.post(url, data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_004_post_role_via_auth(self):
        # curl -s -D- -u admin:admin -X POST -d '{"role":"test2","can_write":true,"access_to":"*"}' -H 'Content-type: application/json' http://127.0.0.1:5000/api/v1/roles
        url = '/api/v1/roles'
        data = {
            'role': role_2,
            'can_write': True,
            'access_to': '*'
        }
        response = self.app.post(url, data = json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_005_get_role_via_api(self):
        # curl -s -D- -X GET http://127.0.0.1:5000/api/v1/roles/test1?api_key=zqg81ge585t0bt3qe0sjj1idvw7hv7vfgc11dsq6
        url = '/api/v1/roles/{}?api_key={}'.format(role_1, api_key)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_006_get_role_via_auth(self):
        # curl -s -D- -u admin:admin -X GET http://127.0.0.1:5000/api/v1/roles/test2
        url = '/api/v1/roles/{}'.format(role_2)
        response = self.app.get(url, headers = headers)
        self.assertEqual(response.status_code, 200)




    def test_009_delete_role_via_api(self):
        # curl -s -D- -X DELETE http://127.0.0.1:5000/api/v1/roles/test1?api_key=zqg81ge585t0bt3qe0sjj1idvw7hv7vfgc11dsq6
        url = '/api/v1/roles/{}?api_key={}'.format(role_1, api_key)
        response = self.app.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_00a_delete_role_via_auth(self):
        # curl -s -D- -u admin:admin -X DELETE http://127.0.0.1:5000/api/v1/roles/test2
        url = '/api/v1/roles/{}'.format(role_2)
        response = self.app.delete(url, headers = headers)
        self.assertEqual(response.status_code, 200)





    def atest_1_api_get_users(self):
        method = 'GET'
        url = '/api/v1/users?api_key={}'.format(api_key)
        print('curl -s -D- -X {} http://127.0.0.1:5000{}'.format(method, url))
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def atest_2_api_get_user(self):
        method = 'POST'
        url = '/api/v1/users/{}?api_key={}'.format(self.username, api_key)
        print('curl -s -D- -X {} -d \'{"name":"andrea","email":"andrea.dainese@example.com","username":"andrea","password":"andrea"}\' -H \'Content-type: application/json\' http://127.0.0.1:5000{}'.format(method, url))
        #curl -s -D- -X POST -d '{"name":"andrea","email":"andrea.dainese@example.com","username":"andrea","password":"andrea","roles":[ "admin" ]}' -H 'Content-type: application/json' http://127.0.0.1:5000/api/v1/users?api_key=emml5esk8it58pbq2u8qqskz7jhhjiw6smr0v4vw
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
