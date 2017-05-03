#!/usr/bin/env python3
""" Wrapper for QEMU """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

CONSOLE_PORT = 5005
IFF_NO_PI = 0x1000
IFF_TAP = 0x0002
INTERFACE_LENGTH = 1
LABEL_LENGTH = 2
TAP_BUFFER = 10000
TUNSETNOCSUM = 0x400454c8
TUNSETDEBUG = 0x400454c9
TUNSETIFF = 0x400454ca
TUNSETPERSIST = 0x400454cb
TUNSETOWNER = 0x400454cc
TUNSETLINK = 0x400454cd
UDP_BUFFER = 10000
UDP_PORT = 5005

import array, atexit, fcntl, getopt, logging, os, select, signal, socket, struct, subprocess, sys, time

def decodeTAPFrame(frame):
    """ Decode a TAP frame to components
    Return:
    - INTEGER: src label
    - INTEGER: src interface ID
    - BYTES: payload
    """
    return
    
def decodeUDPPacket(datagram):
    """ Decode an UDP datagram to components
    Return:
    - INTEGER: dst label
    - INTEGER: dst interface ID
    - BYTES: payload
    """
    dst_label = int.from_bytes(datagram[0:LABEL_LENGTH - 1], byteorder = 'little')
    dst_if = int.from_bytes(udp_datagram[LABEL_LENGTH:LABEL_LENGTH + INTERFACE_LENGTH - 1], byteorder='little')
    logging.debug('UDP packet for label={} iface={} payload={}'.format(dst_label, dst_if, sys.getsizeof(payload)))

def encodeTAPFrame(datagram):
    """ Encode data to be sent via TAP """
    return

def encodeUDPPacket(datagram):
    """ Encode data to be sent via UDP to the router """
    return

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
    print('    -c controller  the IP or domain name of the controller host')
    print('    -l label       an integer starting from 0')
    print('    -x veths       list of comma-separated management veths')
    sys.exit(255)

def main():
    controller = None
    label = None
    inputs = []
    outputs = []
    taps = []
    mgmt_veths = []

    if len(sys.argv) < 2:
        usage()

    # Reading options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dc:l:x:')
    except getopt.GetoptError as err:
        sys.stderr.write('ERROR: {}\n'.format(err))
        usage()
        sys.exit(255)
    for opt, arg in opts:
        if opt == '-d':
            logging.basicConfig(level = logging.DEBUG)
        elif opt == '-c':
            controller = arg
        elif opt == '-l':
            try:
                label = int(arg)
            except Exception as err:
                logging.error('label not recognized')
                sys.exit(255)
        elif opt == '-x':
            try:
                mgmt_veths = arg.split(',')
            except Exception as err:
                logging.error('management veths not recognized')
                sys.exit(255)
        else:
            assert False, 'unhandled option'

    # Checking options
    if controller == None:
        logging.error('controller not recognized')
        sys.exit(255)
    if label == None:
        logging.error('label not recognized')
        sys.exit(255)

    # Preparing socket (controller -> wrapper)
    try:
        from_controller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        from_controller.bind(('', UDP_PORT))
    except Exception as err:
        logging.error('cannot open UDP socket on port {}'.format(UDP_PORT))
        sys.exit(1)
    inputs.append(from_controller)
    atexit.register(from_controller.close)

    # Preparing socket (wrapper -> controller)
    try:
        to_controller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as err:
        logging.error('cannot prepare socket for controller')
        sys.exit(1)
    atexit.register(to_controller.close)

    # Preparing tap
    for tap in os.listdir('/sys/class/net'):
        if tap.startswith('veth') and tap not in mgmt_veths:
            taps.append(tap)
    for tap in taps:
        try:
            from_tun = open('/dev/net/tun', 'r+b', buffering = 0)
            ifr = struct.pack('16sH', tap.encode(), IFF_TAP | IFF_NO_PI)
            fcntl.ioctl(from_tun, TUNSETIFF, ifr)
            fcntl.ioctl(from_tun, TUNSETNOCSUM, 1)
        except Exception as err:
            logging.error('cannot open TUN/TAP descriptor ({})'.format(tap))
            sys.exit(1)
        atexit.register(from_tun.close)
        inputs.append(from_tun)



    # Starting QEMU
    try:
        qemu_cmd = sys.argv[sys.argv.index('--') + 1:]
    except:
        logging.error('no QEMU command to start')
        sys.exit(1)
    logging.info('starting: {}'.format(qemu_cmd))
    sys.exit(0)
    try:
        iol = subprocess.Popen([ iol_bin ] + iol_args, env = iol_env, cwd = os.path.dirname(iol_bin), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 0)
    except Exception as err:
        logging.error('cannot start IOL process')
        sys.exit(1)
    atexit.register(subprocessTerminate, iol)

    # Executing
    while inputs:
        logging.debug('waiting for data')

        if iol.poll() != None:
            logging.error('IOL process died')
            # Grab all output before exiting
            console_history += iol.stderr.read()
            console_history += iol.stdout.read()
            break

        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        if to_iol == None:
            try:
                to_iol = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                to_iol.connect(write_fsocket)
                atexit.register(to_iol.close)
            except Exception as err:
                logging.error('cannot connect to IOL socket')
                to_iol = None
                pass

        for s in readable:
            if s is from_iol:
                logging.debug('data from IOL (TAP)')
                iol_datagram = from_iol.recv(IOL_BUFFER)
                if not iol_datagram:
                    logging.error('cannot receive data from IOL node')
                    break
                else:
                    src_id, src_if, dst_id, dst_if, padding, payload = decodeIOLPacket(iol_datagram)
                    if src_if == MGMT_ID:
                        logging.debug('sending data to MGMT')
                        try:
                            os.write(from_tun.fileno(), payload)
                        except Exception as err:
                            logging.error('cannot send data to MGMT')
                            break
                    else:
                        logging.debug('sending data to controller')
                        try:
                            to_controller.sendto(encodeUDPPacket(label, src_if, payload), (controller, UDP_PORT))
                        except Exception as err:
                            loggin.error('cannot send data to controller')
                            break
            elif s is from_controller:
                logging.debug('data from controller')
                udp_datagram, src_addr = from_controller.recvfrom(UDP_BUFFER)
                if not udp_datagram:
                    logging.error('cannot receive data from controller')
                    sys.exit(1)
                else:
                    label, iface, payload = decodeUDPPacket(udp_datagram)
                    if 'to_iol' != None:
                        try:
                            to_iol.send(encodeIOLPacket(wrapper_id, iol_id, iface, payload))
                        except Exception as err:
                            logging.error('cannot send data to IOL node')
                            break
                    else:
                        logging.error('cannot connect to IOL socket, packet dropped')
            elif s is from_tun:
                logging.debug('data from MGMT')
                try:
                    tap_datagram = array.array('B', os.read(from_tun.fileno(), TAP_BUFFER))
                except Exception as err:
                    logging.error('cannot read data from MGMT')
                    break
                if to_iol != None:
                    try:
                        to_iol.send(encodeIOLPacket(wrapper_id, iol_id, MGMT_ID, tap_datagram))
                    except Exception as err:
                        logging.error('cannot send data to IOL MGMT')
                        break
                else:
                    logging.error('cannot connect to IOL socket, packet dropped')
            elif s is iol.stdout.fileno():
                logging.debug('data from IOL console (stdout)')
                try:
                    data = iol.stdout.read(1)
                except Exception as err:
                    logging.error('cannot read data from IOL console (stdout)')
                if time.time() - alive < MIN_TIME:
                    # Saving console if IOL crashes too soon
                    console_history += data
                inputs, clients = terminalServerSend(inputs, clients, data)
            elif s is iol.stderr.fileno():
                logging.debug('data from IOL console (stderr)')
                try:
                    data = iol.stderr.read(1)
                except Exception as err:
                    logging.error('cannot read data from IOL console (stderr)')
                if time.time() - alive < MIN_TIME:
                    # Saving console if IOL crashes too soon
                    console_history += data
                inputs, clients = terminalServerSend(inputs, clients, data)
            elif s is ts:
                # New client
                inputs, clients = terminalServerAccept(s, inputs, clients, title)
            elif s in clients:
                logging.debug('data from terminal server client')
                data, inputs, clients = terminalServerReceive(s, inputs, clients)
                if data != None:
                    try:
                        iol.stdin.write(data)
                    except Exception as err:
                        logging.error('cannot send data to IOL console')
                        break
            else:
                logging.error('unknown source from select')

    # Terminating
    inputs, clients = terminalServerClose(inputs, clients)
    if time.time() - alive < MIN_TIME:
        # IOL died prematurely
        logging.error('IOL process died prematurely\n')
        print(console_history.decode("utf-8") )
        sys.exit(1)
    else:
        # IOL died after a reasonable time
        sys.exit(0)

if __name__ == '__main__':
    alive = time.time()
    signal.signal(signal.SIGINT, exitGracefully)
    signal.signal(signal.SIGTERM, exitGracefully)
    main()

