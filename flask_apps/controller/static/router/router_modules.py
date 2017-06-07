#!/usr/bin/env python3
""" Modules for router """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import json, logging, requests, time, urllib3
urllib3.disable_warnings()

def routerGetConfig(local_id, controller, api_key):
    while True:
        try:
            routing = requests.get('https://{}/api/v1/routing?api_key={}'.format(controller, api_key), verify = False).json()
            routers = requests.get('https://{}/api/v1/routers?api_key={}'.format(controller, api_key), verify = False).json()
            nodes = requests.get('https://{}/api/v1/routers/{}?api_key={}'.format(controller, local_id, api_key), verify = False).json()['data'][str(local_id)]['labels']
            break
        except:
            logging.error('Cannot get data from controller')
            time.sleep(5)
            continue

    return routing, routers, nodes

