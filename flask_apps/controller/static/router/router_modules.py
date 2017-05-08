#!/usr/bin/env python3
""" Modules for router """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

BUFFER = 10000
INTERFACE_LENGTH = 1
LABEL_LENGTH = 2
PORT = 5005

import json, urllib.request

def routerGetConfig(local_id, master_url, docker_ip):
    with urllib.request.urlopen('{}/api/v1/routing'.format(master_url)) as url:
        routing_table = json.loads(url.read().decode())['data']
    with urllib.request.urlopen('{}/api/v1/controllers'.format(master_url)) as url:
        controller_table = json.loads(url.read().decode())['data']
    with urllib.request.urlopen('http://{}:4243/containers/json?name=node_'.format(docker_ip)) as url:
        nodes_table = json.loads(url.read().decode())
    forwarding_table = []
    print(nodes_table)
    #for route in routing_table:
        #if route['dst_controller'] == local_id:
        #    # Destination is local -> query Docker
        #    try:
        #        with urllib.request.urlopen('http://{}:4243/containers/node_{}/json'.format(controller_table[str(route['dst_controller'])]['docker_ip'], route['dst_label'])) as url:
        #            node_ip = json.loads(url.read().decode())['NetworkSettings']['IPAddress']
        #            route['dst_ip'] = node_ip
        #    except:
        #        # Docker node does not exists -> skip
        #        pass
        #else:
        #    # Destination is remote
        #    route['dst_ip'] = controller_table[str(route['dst_controller'])]['outside_ip']
        #forwarding_table.append(route)
    return forwarding_table

