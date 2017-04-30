#!/usr/bin/env python3
""" Router """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import json, urllib.request

def routerGetConfig(local_id, master_url, api_key):
    with urllib.request.urlopen('{}/api/v1/routing?api_key={}'.format(master_url, api_key)) as url:
        routing_table = json.loads(url.read().decode())['data']
    with urllib.request.urlopen('{}/api/v1/controllers?api_key={}'.format(master_url, api_key)) as url:
        controller_table = json.loads(url.read().decode())['data']
    forwarding_table = []
    for route in routing_table:
        if route['dst_controller'] == local_id:
            # Destination is local -> query Docker
            try:
                with urllib.request.urlopen('http://{}:4243/containers/node_{}/json'.format(controller_table[str(route['dst_controller'])]['docker_ip'], route['dst_label'])) as url:
                    node_ip = json.loads(url.read().decode())['NetworkSettings']['IPAddress']
                    route['dst_ip'] = node_ip
            except:
                # Docker node does not exists -> skip
                pass
        else:
            # Destination is remote
            route['dst_ip'] = controller_table[str(route['dst_controller'])]['outside_ip']
        forwarding_table.append(route)
    return forwarding_table

def router_main(id = None, master_url = None, api_key = None):
    # if receive HUP reload conf, should do every node start, because ip can changes
    print(routerGetConfig(id, master_url, api_key))
