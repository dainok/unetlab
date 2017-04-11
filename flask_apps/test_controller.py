#!/usr/bin/env python3
""" Tests for controller app """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from controller import app, api_key
import os, json, random, tempfile, unittest

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.username = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(10))
        self.password = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
        self.app = app.test_client()

    def test_1_api_get_users(self):
        method = 'GET'
        url = '/api/v1/users?api_key={}'.format(api_key)
        print('curl -s -D- -X {} http://127.0.0.1:5000{}'.format(method, url))
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_2_api_get_user(self):
        method = 'POST'
        url = '/api/v1/users/{}?api_key={}'.format(self.username, api_key)
        print('curl -s -D- -X {} -d \'{"name":"andrea","email":"andrea.dainese@example.com","username":"andrea","password":"andrea"}\' -H \'Content-type: application/json\' http://127.0.0.1:5000{}'.format(method, url))
        #curl -s -D- -X POST -d '{"name":"andrea","email":"andrea.dainese@example.com","username":"andrea","password":"andrea","roles":[ "admin" ]}' -H 'Content-type: application/json' http://127.0.0.1:5000/api/v1/users?api_key=emml5esk8it58pbq2u8qqskz7jhhjiw6smr0v4vw
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
