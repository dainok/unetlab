#!/usr/bin/env python3
""" Wrapper for QEMU """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

API_PORT = 5000
BUFFER = 10000
IFF_NO_PI = 0x1000
IFF_TAP = 0x0002
INTERFACE_LENGTH = 1
LABEL_LENGTH = 2
MIN_TIME = 5
ROUTER_PORT = 5005
TUNSETNOCSUM = 0x400454c8
TUNSETDEBUG = 0x400454c9
TUNSETIFF = 0x400454ca
TUNSETPERSIST = 0x400454cb
TUNSETOWNER = 0x400454cc
TUNSETLINK = 0x400454cd

import array, atexit, fcntl, getopt, logging, os, select, signal, struct, subprocess, sys, time

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
    logging.debug('UDP packet for label={} iface={} payload={}'.format(dst_label, dst_if, sys.getsizeof(payload)))
    return dst_label, dst_if, payload

def encodeUDPPacket(node_id, iface_id, payload):
    """ Encode components to an UDP datagram
    Return:
    - BYTES: UDP datagram
    """
    return node_id.to_bytes(LABEL_LENGTH, byteorder='little') + iface_id.to_bytes(INTERFACE_LENGTH, byteorder='little') + payload

def exitGracefully(signum, frame):
    """ Trap CTRL+C and TERM signal
    Return:
    - sys.exit(0): with SIGINT and SIGTERM
    """
    import sys
    logging.debug('signum {} received'.format(signum))
    if signum == 2 or signum == 15:
        logging.error('terminating')
        sys.exit(0)

def subprocessTerminate(process):
    """ Terminate the subprocess if running """
    if process.poll() == None:
        process.terminate()

def usage():
    print('Usage: {} [OPTIONS] -- [QEMU CMD]'.format(sys.argv[0]))
    print('')
    print('Options:')
    print('    -d             enable debug')
    print('    -r router      the IP or domain name of the router')
    print('    -l label       an integer starting from 0')
    print('    -m veths       management interfaces')
    sys.exit(255)

def main():
    import socket
    console_history = bytearray()
    router = None
    label = None
    inputs = []
    outputs = []
    mgmt_veths = []
    veths = {}

    if len(sys.argv) < 2:
        usage()

    # Reading options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dr:l:m:')
    except getopt.GetoptError as err:
        sys.stderr.write('ERROR: {}\n'.format(err))
        usage()
        sys.exit(255)
    for opt, arg in opts:
        if opt == '-d':
            logging.basicConfig(level = logging.DEBUG)
        elif opt == '-r':
            router = arg
        elif opt == '-l':
            try:
                label = int(arg)
            except Exception as err:
                logging.error('label not recognized')
                logging.error(err)
                sys.exit(255)
        elif opt == '-m':
            mgmt_veths.append(arg)
        else:
            assert False, 'unhandled option'

    # Checking options
    if router == None:
        logging.error('router not recognized')
        sys.exit(255)
    if label == None:
        logging.error('label not recognized')
        sys.exit(255)
    try:
        qemu_cmd = sys.argv[sys.argv.index('--') + 1:]
    except:
        logging.error('no QEMU command to start')
        sys.exit(1)

    # Preparing socket (router -> wrapper)
    from_router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    from_router.bind(('', ROUTER_PORT))
    try:
        from_router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        from_router.bind(('', ROUTER_PORT))
    except Exception as err:
        logging.error('cannot open UDP socket on port {}'.format(ROUTER_PORT))
        logging.error(err)
        sys.exit(1)
    inputs.append(from_router)
    atexit.register(from_router.close)

   # Preparing socket (wrapper -> router)
    try:
        to_router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as err:
        logging.error('cannot prepare socket for router')
        logging.error(err)
        sys.exit(1)
    atexit.register(to_router.close)

    # Preparing tap (wrapper <-> node)
    for tap in os.listdir('/sys/class/net'):
        if tap.startswith('veth'):
            try:
                from_tun = open('/dev/net/tun', 'r+b', buffering = 0)
                ifr = struct.pack('16sH', tap.encode(), IFF_TAP | IFF_NO_PI)
                fcntl.ioctl(from_tun, TUNSETIFF, ifr)
                fcntl.ioctl(from_tun, TUNSETNOCSUM, 1)
            except Exception as err:
                logging.error('cannot open TUN/TAP descriptor ({})'.format(tap))
                logging.error(err)
                sys.exit(1)
            atexit.register(from_tun.close)
            inputs.append(from_tun)
            veths[int(tap[4:])] = from_tun

    # Starting QEMU
    logging.info('starting: {}'.format(' '.join(qemu_cmd)))
    try:
        p = subprocess.Popen(qemu_cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 0)
        time.sleep(0.5)
    except Exception as err:
        logging.error('cannot start QEMU process')
        logging.error(err)
        sys.exit(1)
    atexit.register(subprocessTerminate, p)

    # Executing
    while inputs:
        logging.debug('waiting for data')

        if p.poll() != None:
            logging.error('QEMU process died')
            # Grab all output before exiting
            console_history += p.stderr.read()
            console_history += p.stdout.read()
            break

        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            if s is from_router:
                logging.debug('data from router')
                udp_datagram, src_addr = from_router.recvfrom(BUFFER)
                if not udp_datagram:
                    logging.error('cannot receive data from router')
                    sys.exit(1)
                else:
                    label, iface, payload = decodeUDPPacket(udp_datagram)
                    if not iface in veths:
                        logging.debug('dropping data for management interface (veth{})'.format(iface))
                        continue
                    try:
                        logging.debug('sending data to QEMU port veth{}'.format(iface))
                        os.write(veths[iface].fileno(), payload)
                    except Exception as err:
                        logging.error('cannot send data to QEMU port veth{}'.format(iface))
                        logging.error(err)
                        break
            else:
                veth_found = False
                for interface_id in veths:
                    if s is veths[interface_id]:
                        logging.debug('data from QEMU port {}'.format(interface_id))
                        veth_found = True
                        datagram = os.read(s.fileno(), BUFFER)
                        if not datagram:
                            logging.error('cannot receive data from router')
                            sys.exit(1)
                        else:
                            try:
                                logging.debug('sending data to router {} ({}:{})'.format(router, label, interface_id))
                                to_router.sendto(encodeUDPPacket(label, interface_id, datagram), (router, ROUTER_PORT))
                                break
                            except Exception as err:
                                logging.error('cannot send data to router')
                                logging.error(err)
                                sys.exit(1)
                if veth_found == False:
                    logging.error('unknown source from select')

    # Terminating
    if time.time() - alive < MIN_TIME:
        # QEMU died prematurely
        logging.error('QEMU process died prematurely\n')
        logging.error(console_history.decode('utf-8'))
        sys.exit(1)
    else:
        # QEMU died after a reasonable time
        sys.exit(0)

if __name__ == '__main__':
    alive = time.time()
    signal.signal(signal.SIGINT, exitGracefully)
    signal.signal(signal.SIGTERM, exitGracefully)
    main()

