#!/usr/bin/env python3
""" Wrapper modules """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170105'

CONSOLE_PORT = 5005
IFF_NO_PI = 0x1000
IFF_TAP = 0x0002
IOL_BUFFER = 1600
MGMT_ID = 0
MGMT_NAME = 'veth0'
MIN_TIME = 5
TAP_BUFFER = 10000
TS_BUFFER = 1
TUNSETNOCSUM = 0x400454c8
TUNSETDEBUG = 0x400454c9
TUNSETIFF = 0x400454ca
TUNSETPERSIST = 0x400454cb
TUNSETOWNER = 0x400454cc
TUNSETLINK = 0x400454cd
UDP_BUFFER = 10000
UDP_PORT = 5005
LABEL_BITS = 32

#--[ Telnet Commands ]--------------------------------------------------------
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
#--[ Telnet Options ]---------------------------------------------------------
BINARY =  0 # Transmit Binary
ECHO   =  1 # Echo characters back to sender
RECON  =  2 # Reconnection
SGA    =  3 # Suppress Go-Ahead
TTYPE  = 24 # Terminal Type
NAWS   = 31 # Negotiate About Window Size
LINEMO = 34 # Line Mode

import logging

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
    import sys
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

def decodeUDPPacket(udp_datagram):
    """ Decode an UDP datagram to components
    Return:
    - INTEGER: node_id
    - INTEGER: interface ID
    - BYTES: payload
    """
    import sys
    # UDP datagram format:
    # - 24 bits for the node LABEL (up to 16M of nodes)
    # - 8 bits for the interface ID (up to 256 of per node interfaces)
    node_id = int.from_bytes(udp_datagram[0:2], byteorder='little')
    iface_id = int(udp_datagram[3])
    payload = udp_datagram[4:]
    logging.debug('UDP packet label={} iface={} payload={}'.format(label, iface, sys.getsizeof(payload)))
    return node_id, iface_id, payload

def encodeUDPPacket(node_id, iface_id, payload):
    """ Encode components to an UDP datagram
    Return:
    - BYTES: UDP datagram
    """
    return node_id.to_bytes(3, byteorder='little') + iface_id.to_bytes(1, byteorder='little') + payload

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

def isLabel(label):
    """ Check if an interer is valid as a label
    Return:
    True: if 0 <= integer <= LABEL_BITS ^ 2 - 1
    False: otherwise
    """
    try:
        if label < 0 or label > LABEL_BITS ** 2 - 1:
            logging.debug('label {} is not valid'.format(label))
            return False
    except Exception as err:
        logging.debug('label {} is not an integer'.format(label))
        logging.debug(err)
        return False
    return True

def subprocessTerminate(process):
    """ Terminate the subprocess if running """
    if process.poll() == None:
        process.terminate()

def terminalServerAccept(client, inputs, clients, title):
    """ Accept a terminal server client and store the descriptor
    Return:
    - DICT: list of descriptors (input)
    - DICT: list of descriptors (client)
    """
    import socket
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
    import socket
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
    import socket
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
    import socket
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
    import socket
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ts.bind(('', CONSOLE_PORT))
        ts.listen(1)
    except Exception as err:
        return False
    return ts

