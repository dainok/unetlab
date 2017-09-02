#!/usr/bin/env python3
""" Router """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

BUFFER = 10000
INTERFACE_LENGTH = 1
LABEL_LENGTH = 2
ROUTER_PORT = 5005

import atexit, getopt, logging, select, signal, sys
import router_modules

router_id = None
controller = None
api_key = None

def decodeUDPPacket(datagram):
    """ Decode an UDP datagram to components
    Return:
    - INTEGER: dst label
    - INTEGER: dst interface ID
    - BYTES: payload
    """
    dst_label = int.from_bytes(datagram[0:LABEL_LENGTH], byteorder = 'little')
    dst_if = int.from_bytes(datagram[LABEL_LENGTH:LABEL_LENGTH + INTERFACE_LENGTH], byteorder='little')
    payload = datagram[LABEL_LENGTH + INTERFACE_LENGTH:]
    logging.debug('UDP packet from label={} iface={} payload={}'.format(dst_label, dst_if, sys.getsizeof(payload)))
    return dst_label, dst_if, payload

def encodeUDPPacket(node_id, iface_id, payload):
    """ Encode components to an UDP datagram
    Return:
    - BYTES: UDP datagram
    """
    return node_id.to_bytes(LABEL_LENGTH, byteorder='little') + iface_id.to_bytes(INTERFACE_LENGTH, byteorder='little') + payload

def exitGracefully(signum, frame):
    global controller, router_id
    """ Trap CTRL+C and TERM signal
    Return:
    - sys.exit(0): with SIGINT and SIGTERM
    """
    logging.debug('signum {} received'.format(signum))
    if signum == 2 or signum == 15:
        logging.error('terminating')
        sys.exit(0)
    if signum == 1:
        logging.error('reloading')
        routing, routers, nodes = router_modules.routerGetConfig(router_id, controller, api_key)

def usage():
    print('Usage: {} [OPTIONS] -- [QEMU CMD]'.format(sys.argv[0]))
    print('')
    print('Options:')
    print('    -d             enable debug')
    print('    -c controller  the IP or domain name of the controller host')
    print('    -i id          an integer starting from 0')
    print('    -k key         API key')
    sys.exit(255)

def main():
    import socket
    global api_key, controller, router_id
    inputs = []
    outputs = []

    if len(sys.argv) < 2:
        usage()

    # Reading options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dc:i:k:')
    except getopt.GetoptError as err:
        sys.stderr.write('ERROR: {}\n'.format(err))
        usage()
        sys.exit(255)
    for opt, arg in opts:
        if opt == '-d':
            logging.basicConfig(level = logging.DEBUG)
        elif opt == '-c':
            controller = arg
        elif opt == '-i':
            try:
                router_id = int(arg)
            except Exception as err:
                logging.error('ID not recognized')
                logging.error(err)
                sys.exit(255)
        elif opt == '-k':
            api_key = arg
        else:
            assert False, 'unhandled option'

    # Checking options
    if controller == None:
        logging.error('controller not set')
        sys.exit(255)
    if router_id == None:
        logging.error('label not set')
        sys.exit(255)
    if api_key == None:
        logging.error('API key not set')
        sys.exit(255)

    # Loading configuration
    routing, routers, nodes = router_modules.routerGetConfig(router_id, controller, api_key)

    # Preparing socket
    ingress = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ingress.bind(('', ROUTER_PORT))
    try:
        ingress = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ingress.bind(('', ROUTER_PORT))
    except Exception as err:
        logging.error('cannot open UDP socket on port {}'.format(ROUTER_PORT))
        logging.error(err)
        sys.exit(1)
    inputs.append(ingress)
    atexit.register(ingress.close)

   # Preparing socket (wrapper -> controller)
    try:
        egress = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as err:
        logging.error('cannot prepare socket for egress packtes')
        logging.error(err)
        sys.exit(1)
    atexit.register(egress.close)

    # Executing
    while inputs:
        logging.debug('waiting for data')

        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            if s is ingress:
                logging.debug('ingress data')
                udp_datagram, src_addr = ingress.recvfrom(BUFFER)
                if not udp_datagram:
                    logging.error('cannot receive data from remote router/wrapper')
                    sys.exit(1)
                else:
                    label, iface, payload = decodeUDPPacket(udp_datagram)
                    try:
                        dst_router_id = routing[str(label)][str(iface)]['dst_router']
                        dst_label = routing[str(label)][str(iface)]['dst_label']
                        dst_if = routing[str(label)][str(iface)]['dst_if']
                        if router_id == dst_router_id:
                            dst_node_ip = nodes[str(dst_label)]['ip']
                            dst_router_ip = None
                        else:
                            dst_node_ip = None
                            dst_router_ip = routers[str(dst_router_id)]['outside_ip']
                    except:
                        logging.debug('cannot lookup routing table ({}:{})'.format(label, iface))
                        continue

                    if dst_router_id == router_id:
                        # Local destination
                        egress.sendto(encodeUDPPacket(dst_label, dst_if, payload), (dst_node_ip, ROUTER_PORT))
                        logging.debug('packet sent to local router ({}:{})'.format(dst_label, dst_if))
                    else:
                        # Remote destination
                        egress.sendto(encodeUDPPacket(label, iface, payload), (dst_router_ip, ROUTER_PORT))
                        logging.debug('packet sent to remote router ({}:{})'.format(dst_router_ip, ROUTER_PORT))
            else:
                logging.error('unknown source from select')

    # Terminating
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGHUP, exitGracefully)
    signal.signal(signal.SIGINT, exitGracefully)
    signal.signal(signal.SIGTERM, exitGracefully)
    main()

