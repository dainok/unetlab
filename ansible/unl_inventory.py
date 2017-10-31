#!/usr/bin/env python3.5
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20171031'

import json, logging, os, requests, urllib3, sys
urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level = logging.WARNING)

unl_controller = os.environ.get('UNL_CONTROLLER')
unl_apikey = os.environ.get('UNL_APIKEY')
unl_lab = os.environ.get('UNL_LAB')

if not unl_controller:
    logging.error('Variable UNL_CONTROLLER is not set')
    sys.exit(1)
if not unl_apikey:
    logging.error('Variable UNL_APIKEY is not set')
    sys.exit(1)
if not unl_lab:
    logging.error('Variable UNL_LAB is not set')
    sys.exit(1)

master_url = 'https://{}'.format(unl_controller)
master_key = '?api_key=zqg81ge585t0bt3qe0sjj1idvw7hv7vfgc11dsq6'

# Checking if the controller is available
try:
    r = requests.get('{}/'.format(master_url), verify = False)
except:
    logging.error('UNetLabv2 controller is not available')
    sys.exit(1)

r = requests.get('{}/api/v1/labs/{}{}'.format(master_url, unl_lab, master_key), verify = False)
if r.status_code != 200:
    logging.error('Cannot get lab "{}"'.format(unl_lab))
    sys.exit(1)
data = r.json()
jlab = data['data'][unl_lab]

joutput = {
    '_meta': {
        'hostvars': {}
    },
    'all': {
        'hosts': []
    }
}

try:
    for node_id, node in jlab['topology']['nodes'].items():
        joutput['_meta']['hostvars'][node['name']] = {
            'ansible_host': node['ip']
        }
        joutput['all']['hosts'].append(node['name'])
except:
    pass
print(json.dumps(joutput, sort_keys = True, indent = 4))
