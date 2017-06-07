#!/usr/bin/env python3
""" Tests for controller app """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

from controller import app, api_key
import base64, json, os, random, tempfile, unittest

admin_username = 'admin'
admin_password = 'admin'

role_1 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(7))
username_1 = 'z' + ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(9))
password_1 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))
password_2 = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(20))

class FlaskTestCase(unittest.TestCase):
    lab_id = None

    def setUp(self):
        self.app = app.test_client()

    """
    Tests about labs
    """

    def test_04_00_post_lab_via_api(self):
        # curl -s -D- -X POST -d '{"name":"Test","repository":"local","version":1,"author":"Tester","topology":{"nodes":{"0":{"name":"NodeA","type":"qemu","subtype":"vyos","image":"dainok/node-vyos:1.1.7","ethernet":3,"ram":1024,"icon":"router.png","left":100,"top":100,"interfaces":{"0":{"name":"eth0","management":"TRUE"},"1":{"name":"eth1","connection":0},"2":{"name":"eth2","connection":2,"delay":100,"drop":50,"jitter":3}}},"1":{"name":"NodeB","type":"qemu","subtype":"vyos","image":"dainok/node-vyos:1.1.7","ethernet":3,"ram":1024,"icon":"router.png","left":100,"top":100,"interfaces":{"0":{"name":"eth0","management":"TRUE"},"1":{"name":"eth1","connection":0},"2":{"name":"eth2","connection":1}}},"2":{"name":"NodeC","type":"qemu","subtype":"vyos","image":"dainok/node-vyos:1.1.7","ethernet":3,"ram":1024,"icon":"router.png","left":100,"top":100,"interfaces":{"0":{"name":"eth0","management":"TRUE"},"1":{"name":"eth1","connection":1},"2":{"name":"eth2","connection":2}}}},"connections":{"0":{"type":"ethernet","shutdown":"FALSE"},"1":{"type":"ethernet","shutdown":"FALSE"},"2":{"type":"serial","shutdown":"FALSE"}}}}' -H 'Content-type: application/json' 'http://127.0.0.1:5000/api/v1/labs?commit=true&api_key=zqg81ge585t0bt3qe0sjj1idvw7hv7vfgc11dsq6'
        url = '/api/v1/labs?commit=true&api_key={}'.format(api_key)
        data = {
            'name': 'Test',
            'repository': 'local',
            'version': 1,
            'author': 'Tester',
            'topology': {
                'nodes': {
                    '0': {
                        'name': 'NodeA',
                        'type': 'iol',
                        'image': 'aaa',
                        'ethernet': 3,
                        'serial': 1,
                        'ram': 1024,
                        'icon': 'router.png',
                        'left': 100,
                        'top': 100,
                        'interfaces': {
                            '0': {
                                'name': 'e0/0',
                                'connection': 0,
                                'delay': 100,
                                'drop': 50,
                                'jitter': 3
                            },
                            '1': {
                                'name': 's0/0',
                                'connection': 2,
                                'delay': 100,
                                'drop': 50,
                                'jitter': 3
                            }
                        }
                    },
                    '1': {
                        'name': 'NodeB',
                        'type': 'iol',
                        'image': 'aaa',
                        'ethernet': 3,
                        'serial': 1,
                        'ram': 1024,
                        'icon': 'router.png',
                        'left': 100,
                        'top': 100,
                        'interfaces': {
                            '0': {
                                'name': 'e0/0',
                                'connection': 0,
                                'delay': 100,
                                'drop': 50,
                                'jitter': 3
                            },
                            '1': {
                                'name': 'e0/0',
                                'connection': 1,
                                'delay': 100,
                                'drop': 50,
                                'jitter': 3
                            }
                        }
                    },
                    '2': {
                        'name': 'NodeC',
                        'type': 'iol',
                        'image': 'aaa',
                        'ethernet': 3,
                        'serial': 1,
                        'ram': 1024,
                        'icon': 'router.png',
                        'left': 100,
                        'top': 100,
                        'interfaces': {
                            '0': {
                                'name': 'e0/0',
                                'connection': 1,
                                'delay': 100,
                                'drop': 50,
                                'jitter': 3
                            },
                            '1': {
                                'name': 's0/0',
                                'connection': 2,
                                'delay': 100,
                                'drop': 50,
                                'jitter': 3
                            }
                        }
                    }
                },
                'connections': {
                    '0': {
                        'type': 'ethernet',
                        'shutdown': False
                    },
                    '1': {
                        'type': 'ethernet',
                        'shutdown': False
                    },
                    '2': {
                        'type': 'serial',
                        'shutdown': False
                    }
                }
            }
        }
        response = self.app.post(url, data = json.dumps(data), content_type = 'application/json')
        response_data = json.loads(response.get_data(as_text = True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data']['version'], 1)
        self.assertEqual(response_data['data']['author'], 'Tester')
        self.assertEqual(response_data['data']['name'], 'Test')
        self.assertEqual(response_data['data']['repository'], 'local')
        self.__class__.lab_id = response_data['data']['id']

    def test_04_01_get_labs_via_api(self):
        # curl -s -D- -X GET http://127.0.0.1:5000/api/v1/labs?api_key=emml5esk8it58pbq2u8qqskz7jhhjiw6smr0v4vw
        url = '/api/v1/labs?commit=true&api_key={}'.format(api_key)
        response = self.app.get(url)
        response_data = json.loads(response.get_data(as_text = True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], 'success')

if __name__ == '__main__':
    unittest.main()
