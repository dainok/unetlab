#!/usr/bin/env python3
""" Wrapper for IOL """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170105'

API_PORT = 5000
BUFFER = 10000
IFF_NO_PI = 0x1000
IFF_TAP = 0x0002
INTERFACE_LENGTH = 1
LABEL_LENGTH = 2
MIN_TIME = 5
ROUTER_PORT = 5005
CONSOLE_PORT = 5023
TS_BUFFER = 1
TUNSETNOCSUM = 0x400454c8
TUNSETDEBUG = 0x400454c9
TUNSETIFF = 0x400454ca
TUNSETPERSIST = 0x400454cb
TUNSETOWNER = 0x400454cc
TUNSETLINK = 0x400454cd

# Telnet Commands
IS     =   0 # Sub-process negotiation IS command
SEND   =   1 # Sub-process negotiation SEND command
SE     = 240 # End of subnegotiation parameters
NOP    = 241 # No operation
DATMK  = 242 # Data stream portion of a sync.
BREAK  = 243 # NVT Character BRK
IP     = 244 # Interrupt Process
AO     = 245 # Abort Output
AYT    = 246 # Are you there
EC     = 247 # Erase Character
EL     = 248 # Erase Line
GA     = 249 # The Go Ahead Signal
SB     = 250 # Sub-option to follow
WILL   = 251 # Will; request or confirm option begin
WONT   = 252 # Wont; deny option request
DO     = 253 # Do = Request or confirm remote option
DONT   = 254 # Don't = Demand or confirm option halt
IAC    = 255 # Interpret as Command
# Telnet Options
BINARY =  0 # Transmit Binary
ECHO   =  1 # Echo characters back to sender
RECON  =  2 # Reconnection
SGA    =  3 # Suppress Go-Ahead
TTYPE  = 24 # Terminal Type
NAWS   = 31 # Negotiate About Window Size
LINEMO = 34 # Line Mode

import array, atexit, fcntl, getopt, logging, os, select, signal, socket, struct, subprocess, sys, time

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

def decodeIOLPacket(iol_datagram):
    """ Decode an IOL datagram to components
    Return:
    - INTEGER: source IOL ID
    - INTEGER: source IOL interface ID
    - INTEGER: destination IOL ID
    - INTEGER: destination IOL interface ID
    - INTEGER: IOL padding
    - BYTES: payload
    """
    # IOL datagram format (maximum observed size is 1555):
    # - 16 bits for the destination IOL ID
    # - 16 bits for the source IOL ID
    # - 8 bits for the destination interface (z = x/y -> z = x + y * 16)
    # - 8 bits for the source interface (z = x/y -> z = x + y * 16)
    # - 16 bits equals to 0x0100
    dst_id = int.from_bytes(iol_datagram[0:2], byteorder='big')
    src_id = int.from_bytes(iol_datagram[2:4], byteorder='big')
    dst_if = iol_datagram[4]
    src_if = iol_datagram[5]
    padding = 256 * iol_datagram[6] + iol_datagram[7]
    payload = iol_datagram[8:]
    logging.debug('IOL packet src={}:{} dst={}:{} padding={} payload={}'.format(src_id, src_if, dst_id, dst_if, padding, sys.getsizeof(payload)))
    return src_id, src_if, dst_id, dst_if, padding, payload

def encodeIOLPacket(src_id, dst_id, iface, payload):
    """ Encode components to an IOL datagram
    Return:
    - BYTES: IOL datagram
    """
    return dst_id.to_bytes(2, byteorder='big') + src_id.to_bytes(2, byteorder='big') + iface.to_bytes(1, byteorder='big') + iface.to_bytes(1, byteorder='big') + (256).to_bytes(2, byteorder='big') + payload

def terminalServerAccept(client, inputs, clients, title):
    """ Accept a terminal server client and store the descriptor
    Return:
    - DICT: list of descriptors (input)
    - DICT: list of descriptors (client)
    """
    conn, addr = client.accept()
    logging.debug('client {}:{} connected'.format(addr[0], str(addr[1])))
    conn.send(bytes([ IAC ]) + bytes([ WILL ]) + bytes([ ECHO ]))
    conn.send(bytes([ IAC ]) + bytes([ WILL ]) + bytes([ SGA ]))
    conn.send(bytes([ IAC ]) + bytes([ WILL ]) + bytes([ BINARY ]))
    conn.send(bytes([ IAC ]) + bytes([ DO ]) + bytes([ BINARY ]))
    if title != None:
        conn.send(b'\033' + b']' + b'0' + b';' + str.encode(title) + b'\007')
    conn.send(str.encode('Welcome {} \r\n'.format(addr[0])))
    inputs.append(conn)
    clients.append(conn)
    return inputs, clients

def terminalServerClose(inputs, clients):
    """ Close all terminal server connections
    Return:
    - DICT: list of descriptors (input)
    - DICT: list of descriptors (client)
    """
    logging.debug('terminating terminal server connections')
    inputs, clients = terminalServerSend(inputs, clients, 'Terminating connection')
    for client in clients:
        client.close()
        inputs.remove(client)
        client.remove(client)
    return inputs, clients

def terminalServerReceive(client, inputs, clients):
    """ Receive data from client
    Return:
    - BYTE: received data
    - DICT: list of descriptors (inputs)
    - DICT: list of descriptors (client)
    """
    logging.debug('receiving data from client')
    try:
        data = client.recv(TS_BUFFER)
        if not data:
            raise Exception()
        if (int.from_bytes(data, byteorder='big') == IAC):
            # Need to pop two more telnet commands
            data = client.recv(TS_BUFFER)
            data = client.recv(TS_BUFFER)
            data = None
    except Exception as err:
        logging.error('cannot receive data from client')
        inputs.remove(client)
        clients.remove(client)
    return data, inputs, clients

def terminalServerSend(inputs, clients, data):
    """ Send data to client
    Return:
    - DICT: list of descriptors (inputs)
    - DICT: list of descriptors (client)
    """
    for client in clients:
        try:
            client.send(data)
        except:
            logging.debug('removing broken client')
            client.close()
            inputs.remove(client)
            clients.remove(client)
    return inputs, clients

def terminalServerStart():
    """ Start the terminal server
    Return:
    - INT: the descriptor if it can start
    - False: otherwise
    """
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ts.bind(('', CONSOLE_PORT))
        ts.listen(1)
    except Exception as err:
        return False
    return ts

def exitGracefully(signum, frame):
    """ Trap CTRL+C and TERM signal
    Return:
    - sys.exit(0): with SIGINT and SIGTERM
    """
    logging.debug('signum {} received'.format(signum))
    if signum == 2 or signum == 15:
        logging.error('terminating')
        sys.exit(0)

def subprocessTerminate(process):
    """ Terminate the subprocess if running """
    if process.poll() == None:
        process.terminate()

def usage():
    print('Usage: {} [OPTIONS] -- [IOL CMD]'.format(sys.argv[0]))
    print('')
    print('Options:')
    print('    -d             enable debug')
    print('    -c controller  the IP or domain name of the controller host')
    print('    -l label       an integer starting from 0')
    print('    -m veths       management interfaces')
    print('    -t             enable terminal server')
    print('    -w title       window title')
    sys.exit(255)

def main():
    clients = []
    console_history = bytearray()
    controller = None
    enable_ts = False
    label = None
    inputs = []
    outputs = []
    mgmt_veths = []
    title = None
    to_iol = None
    veths = {}

    if len(sys.argv) < 2:
        usage()

    # Reading options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'tdc:l:m:w:')
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
                logging.error(err)
                sys.exit(255)
        elif opt == '-m':
            mgmt_veths.append(arg)
        elif opt == '-t':
            enable_ts = True
        elif opt == '-w':
            title = arg
        else:
            assert False, 'unhandled option'

    # Checking options
    if controller == None:
        logging.error('controller not recognized')
        sys.exit(255)
    if label == None:
        logging.error('label not recognized')
        sys.exit(255)
    try:
        iol_cmd = sys.argv[sys.argv.index('--') + 1:]
    except:
        logging.error('no IOL command to start')
        sys.exit(1)
    try:
        iol_id = int(iol_cmd[-1])
        if iol_id == 1024:
            wrapper_id = 1
        else:
            wrapper_id = iol_id + 1
        read_fsocket = '/tmp/netio0/{}'.format(wrapper_id)
        write_fsocket = '/tmp/netio0/{}'.format(iol_id)
    except:
        logging.error('invalid IOL id')
        sys.exit(1)

    # Writing NETMAP
    netmap_file = '/data/node/NETMAP'
    try:
        os.unlink(netmap_file)
    except OSError as err:
        if os.path.exists(netmap_file):
            logging.error('cannot delete existent NETMAP')
            sys.exit(1)
    try:
        netmap_fd = open(netmap_file, 'w')
        for i in range(0, 63):
            netmap_fd.write('{}:{} {}:{}\n'.format(iol_id, i, wrapper_id, i))
        netmap_fd.close()
    except Exception as err:
        logging.error('cannot write NETMAP')
        sys.exit(1)
    atexit.register(os.unlink, netmap_file)

    # Preparing socket (controller -> wrapper)
    from_controller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    from_controller.bind(('', ROUTER_PORT))
    try:
        from_controller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        from_controller.bind(('', ROUTER_PORT))
    except Exception as err:
        logging.error('cannot open UDP socket on port {}'.format(ROUTER_PORT))
        logging.error(err)
        sys.exit(1)
    inputs.append(from_controller)
    atexit.register(from_controller.close)

   # Preparing socket (wrapper -> controller)
    try:
        to_controller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as err:
        logging.error('cannot prepare socket for controller')
        logging.error(err)
        sys.exit(1)
    atexit.register(to_controller.close)

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

    # Preparing socket (IOL -> wrapper)
    try:
        os.unlink(read_fsocket)
    except OSError as err:
        if os.path.exists(read_fsocket):
            logging.error('cannot delete existent socket')
            sys.exit(1)
    try:
        os.makedirs('/tmp/netio0', exist_ok = True)
        from_iol = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        from_iol.bind(read_fsocket)
    except Exception as err:
        logging.error('cannot create file socket {}'.format(read_fsocket))
        sys.exit(1)
    inputs.append(from_iol)
    atexit.register(os.unlink, read_fsocket)

    # Starting IOL
    logging.info('starting: {}'.format(' '.join(iol_cmd)))
    try:
        os.chdir('/data/node')
        p = subprocess.Popen(iol_cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 0)
        time.sleep(0.5)
    except Exception as err:
        logging.error('cannot start IOL process')
        logging.error(err)
        sys.exit(1)
    atexit.register(subprocessTerminate, p)

    # Starting terminal server (after starting the process)
    if enable_ts == True:
        inputs.extend([p.stdout.fileno(), p.stderr.fileno()])
        logging.debug('starting terminal server on {}'.format(CONSOLE_PORT))
        ts = terminalServerStart()
        if ts == False:
            logging.error('terminal server failed to start')
            sys.exit(1)
        atexit.register(ts.close)
        inputs.append(ts)


    # Executing
    while inputs:
        logging.debug('waiting for data')

        if p.poll() != None:
            logging.error('IOL process died')
            # Grab all output before exiting
            console_history += p.stderr.read()
            console_history += p.stdout.read()
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

            if s is from_controller:
                logging.debug('data from controller')
                udp_datagram, src_addr = from_controller.recvfrom(BUFFER)
                if not udp_datagram:
                    logging.error('cannot receive data from controller')
                    sys.exit(1)
                else:
                    label, iface, payload = decodeUDPPacket(udp_datagram)
                    if not iface in veths:
                        logging.debug('dropping data for management interface (veth{})'.format(iface))
                        continue
                    try:
                        logging.debug('sending data to IOL port veth{}'.format(iface))
                        os.write(veths[iface].fileno(), payload)
                    except Exception as err:
                        logging.error('cannot send data to IOL port veth{}'.format(iface))
                        logging.error(err)
                        break

            elif s is from_iol:
                logging.debug('data from IOL (TAP)')
                iol_datagram = from_iol.recv(BUFFER)
                if not iol_datagram:
                    logging.error('cannot receive data from IOL node')
                    break
                else:
                    src_id, src_if, dst_id, dst_if, padding, payload = decodeIOLPacket(iol_datagram)
                    if src_if in mgmt_veths:
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
                            logging.error('cannot send data to controller')
                            break

            elif s is from_tun:
                logging.debug('data from TAP')
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

            elif s is p.stdout.fileno():
                logging.debug('data from IOL console (stdout)')
                try:
                    data = p.stdout.read(1)
                except Exception as err:
                    logging.error('cannot read data from IOL console (stdout)')
                if time.time() - alive < MIN_TIME:
                    # Saving console if IOL crashes too soon
                    console_history += data
                if enable_ts == True:
                    inputs, clients = terminalServerSend(inputs, clients, data)

            elif s is p.stderr.fileno():
                logging.debug('data from IOL console (stderr)')
                try:
                    data = p.stderr.read(1)
                except Exception as err:
                    logging.error('cannot read data from IOL console (stderr)')
                if time.time() - alive < MIN_TIME:
                    # Saving console if IOL crashes too soon
                    console_history += data
                if enable_ts == True:
                    inputs, clients = terminalServerSend(inputs, clients, data)

            elif s is ts:
                logging.debug('new terminal server client')
                inputs, clients = terminalServerAccept(s, inputs, clients, title)

            elif s in clients:
                logging.debug('data from terminal server client')
                data, inputs, clients = terminalServerReceive(s, inputs, clients)
                if data != None:
                    try:
                        p.stdin.write(data)
                    except Exception as err:
                        logging.error('cannot send data to IOL console')
                        break

            else:
                veth_found = False
                for interface_id in veths:
                    if s is veths[interface_id]:
                        logging.debug('data from IOL port {}'.format(interface_id))
                        veth_found = True
                        datagram = os.read(s.fileno(), BUFFER)
                        if not datagram:
                            logging.error('cannot receive data from controller')
                            sys.exit(1)
                        else:
                            try:
                                logging.debug('sending data to controller {} ({}:{})'.format(controller, label, interface_id))
                                to_controller.sendto(encodeUDPPacket(label, interface_id, datagram), (controller, ROUTER_PORT))
                                break
                            except Exception as err:
                                logging.error('cannot send data to controller')
                                logging.error(err)
                                sys.exit(1)
                if veth_found == False:
                    logging.error('unknown source from select')

    # Terminating
    if time.time() - alive < MIN_TIME:
        # IOL died prematurely
        logging.error('IOL process died prematurely\n')
        logging.error(console_history.decode('utf-8'))
        sys.exit(1)
    else:
        # IOL died after a reasonable time
        sys.exit(0)

if __name__ == '__main__':
    alive = time.time()
    signal.signal(signal.SIGINT, exitGracefully)
    signal.signal(signal.SIGTERM, exitGracefully)
    main()

