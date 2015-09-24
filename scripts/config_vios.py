#!/usr/bin/env python3

import os, pexpect, re, sys, time

def now():
    return int(round(time.time() * 1000))

username = 'cisco'
password = 'cisco'
secret = 'cisco'
port = 34179
timeout = 3000
started_at = now()

def node_login(handler):
    # Send an empty line
    handler.sendline('\r\n')
    i = handler.expect([
        'Press RETURN to get started',
        'Username:',
        '\(config',
        '>',
        '#'], timeout = 3)
    if i == 0:
        # Need to send an additional EOL and start node_login() again
        handler.sendline('\r\n')
        return node_login(handler)
    elif i == 1:
        # Need to send username and password
        handler.sendline(username)
        handler.expect('Password:', timeout = 3)
        handler.sendline(password)
        j = handler.expect(['>', '#'], timeout = 3)
        if j == 0:
            # Secret password required
            return node_login(handler)
        elif j == 1:
            # Nothing to do
            return True
        else:
            # Unexpected output
            node_quit(handler)
            return False
    elif i == 2:
        # Config mode detected, need to exit
        handler.sendline('end')
        handler.expect('#', timeout = 3)
        return True
    elif i == 3:
        # Need higher privilege
        handler.sendline('enable')
        j = handler.expect(['Password:', '#'], timeout = 3)
        if j == 0:
            # Need do provide secret
            handler.sendline(secret)
            handler.expect('#', timeout = 3)
            return True
        elif j == 1:
            # Nothing to do
            return True
        else:
            # Unexpected output
            node_quit(handler)
            return False
    elif i == 4:
        # Nothing to do
        return True
    else:
        # Unexpected output
        node_quit(handler)
        return False

def node_quit(handler):
    handler.sendline('quit\n')
    handler.close()

def config_get(handler):
    # Disable paging
    handler.sendline('terminal length 0')
    handler.expect('#', timeout = 3)

    # Getting the config
    handler.sendline('show startup-config')
    handler.expect('#', timeout = 3)
    config = handler.before.decode()

    # Manipulating the config
    config = re.sub('.*Using [0-9]+ out of [0-9]+ bytes\r\n', '', config, flags=re.DOTALL)
    config = re.sub('!\r\nend.*', '!\nend', config, flags=re.DOTALL)

    return config

try:
    while (started_at + timeout > now()):
        handler = pexpect.spawn('telnet 127.0.0.1 %i' %(port))
        time.sleep(0.1)
        if handler.isalive() == True:
            break

    if (handler.isalive() != True):
        print('ERROR: cannot connect to port %i' %(port))
        node_quit(handler)
        sys.exit(1)

    rc = node_login(handler)
    if rc != True:
        print('ERROR: failed to login')
        node_quit(handler)
        sys.exit(2)

    rc = config_get(handler)
    if rc == False:
        print('ERROR: failed to retrieve config')

    node_quit(handler)
    sys.exit(0)
except Exception as e:
    print('ERROR: got an exception')
    print(type(e))  # the exception instance
    print(e.args)   # arguments stored in .args
    print(e)        # __str__ allows args to be printed directly,
    node_quit(handler)
    sys.exit(127)
