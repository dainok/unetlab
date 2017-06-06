#!/usr/bin/env python3.5
""" Modules for router """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

BUFFER = 10000
INTERFACE_LENGTH = 1
LABEL_LENGTH = 2

import aiohttp, asyncio, json

async def get(url):
    async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(verify_ssl = False)) as session:
        async with session.get(url) as response:
            answer = json.loads(await response.text())
            answer['url'] = url
            return answer

def routerGetConfig(local_id, controller, api_key):
    routing = None
    controllers = None
    nodes = None
    tasks = [
            asyncio.ensure_future(get('https://{}/api/v1/routing?api_key={}'.format(controller, api_key))),
            asyncio.ensure_future(get('https://{}/api/v1/routers?api_key={}'.format(controller, api_key))),
            asyncio.ensure_future(get('https://{}/api/v1/routers/{}?api_key={}'.format(controller, local_id, api_key)))
    ]
    loop = asyncio.get_event_loop()
    responses, _ = loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    for response in responses:
        data = response.result()
        if 'routing' in response.result()['url']:
            routing = response.result()['data']
        elif 'controllers/{}'.format(local_id) in response.result()['url']:
            nodes = response.result()['data'][str(local_id)]['labels']
        else:
            controllers = response.result()['data']
    return routing, controllers, nodes

