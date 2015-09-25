#!/usr/bin/env python3

# scripts/config_vios.py
#
# Import/Export script for vIOS.
#
# LICENSE:
#
# This file is part of UNetLab (Unified Networking Lab).
#
# UNetLab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UNetLab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with UNetLab. If not, see <http://www.gnu.org/licenses/>.
#
# @author Andrea Dainese <andrea.dainese@gmail.com>
# @copyright 2014-2015 Andrea Dainese
# @license http://www.gnu.org/licenses/gpl.html
# @link http://www.unetlab.com/
# @version 20150826

import getopt, os, pexpect, re, sys, time

username = 'cisco'
password = 'cisco'
secret = 'cisco'

def node_login(handler, end_before):
    # Send an empty line, and wait for the login prompt
    i = -1
    while (i == -1 or now() > end_before):
        try:
            handler.sendline('\r\n')
            i = handler.expect([
                'Username:',
                '\(config',
                '>',
                '#'], timeout = 1)
        except:
            i = -1

    if i == 0:
        # Need to send username and password
        handler.sendline(username)
        handler.expect('Password:', timeout = end_before - now())
        handler.sendline(password)
        j = handler.expect(['>', '#'], timeout = end_before - now())
        if j == 0:
            # Secret password required
            return node_login(handler, end_before)
        elif j == 1:
            # Nothing to do
            return True
        else:
            # Unexpected output
            node_quit(handler)
            return False
    elif i == 1:
        # Config mode detected, need to exit
        handler.sendline('end')
        handler.expect('#', timeout = end_before - now())
        return True
    elif i == 2:
        # Need higher privilege
        handler.sendline('enable')
        j = handler.expect(['Password:', '#'], timeout = end_before - now())
        if j == 0:
            # Need do provide secret
            handler.sendline(secret)
            handler.expect('#', timeout = end_before - now())
            return True
        elif j == 1:
            # Nothing to do
            return True
        else:
            # Unexpected output
            node_quit(handler)
            return False
    elif i == 3:
        # Nothing to do
        return True
    else:
        # Unexpected output
        node_quit(handler)
        return False

def node_quit(handler):
    handler.sendline('quit\n')
    handler.close()

def config_get(handler, end_before):
    # Disable paging
    handler.sendline('terminal length 0')
    handler.expect('#', timeout = end_before - now())

    # Getting the config
    handler.sendline('show startup-config')
    handler.expect('#', timeout = end_before - now())
    config = handler.before.decode()

    # Manipulating the config
    config = re.sub('\r', '', config, flags=re.DOTALL)                                      # Unix style
    config = re.sub('.*Using [0-9]+ out of [0-9]+ bytes\n', '', config, flags=re.DOTALL)    # Header
    config = re.sub('!\nend.*', '!\nend', config, flags=re.DOTALL)                          # Footer

    return config

def config_put(handler, end_before, config):
    # Got to configure mode
    handler.sendline('configure terminal')
    handler.expect('\(config', timeout = end_before - now())

    # Pushing the config
    for line in config.splitlines():
        handler.sendline(line)
        handler.expect('\r\n')

    # At the end of configuration be sure we are in non config mode (sending CTRl + Z)
    handler.sendline('\x1A')
    handler.expect('#')

    # Save
    handler.sendline('copy running-config startup-config')
    handler.expect('Destination filename', timeout = end_before - now())
    handler.sendline('\r\n')
    handler.expect('#', timeout = end_before - now())

    return True

def usage():
    print('Usage: %s <standard options>' %(sys.argv[0]));
    print('Standard Options:');
    print('-a <s>    *Action can be:')
    print('           - get: get the startup-configuration and push it to a file')
    print('           - put: put the file as startup-configuration')
    print('-f <s>    *File');
    print('-p <n>    *Console port');
    print('-t <n>     Timeout (default = 0)');
    print('* Mandatory option')

def now():
    # Return current UNIX time in milliseconds
    return int(round(time.time() * 1000))

def main():
    action = None
    filename = None
    port = None
    timeout = 0

    # Getting parameters from command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:p:t:f:', ['action=', 'port=', 'timeout=', 'file='])
    except getopt.GetoptError as e:
        usage()
        sys.exit(3)

    for o, a in opts:
        if o in ('-a', '--action'):
            action = a
        elif o in ('-f', '--file'):
            filename = a
        elif o in ('-p', '--port'):
            try:
                port = int(a)
            except:
                port = -1
        elif o in ('-t', '--timeout'):
            try:
                timeout = int(a) * 1000
            except:
                timeout = -1
        else:
            print('ERROR: invalid parameter.')

    # Checking mandatory parameters
    if action == None or port == None or filename == None:
        usage()
        print('ERROR: missing mandatory parameters.')
        sys.exit(1)
    if action not in ['get', 'put']:
        usage()
        print('ERROR: invalid action.')
        sys.exit(1)
    if timeout < 0:
        usage()
        print('ERROR: timeout must be 0 or higher.')
        sys.exit(1)
    if port < 0:
        usage()
        print('ERROR: port must be 32768 or higher.')
        sys.exit(1)
    if action == 'get' and os.path.exists(filename):
        usage()
        print('ERROR: destination file already exists.')
        sys.exit(1)
    if action == 'put' and not os.path.exists(filename):
        usage()
        print('ERROR: source file does not already exist.')
        sys.exit(1)
    if action == 'put':
        try:
            fh = open(filename, 'r')
            config = fh.read()
            fh.close()
        except:
            usage()
            print('ERROR: cannot read from file.')
            sys.exit(1)


    end_before = now() + timeout

    try:
        # Connect to the device
        while (now() < end_before):
            handler = pexpect.spawn('telnet 127.0.0.1 %i' %(port))
            time.sleep(0.1)
            if handler.isalive() == True:
                break

        if (handler.isalive() != True):
            print('ERROR: cannot connect to port "%i".' %(port))
            node_quit(handler)
            sys.exit(2)

        # Login to the device and get a privileged prompt
        rc = node_login(handler, end_before)
        if rc != True:
            print('ERROR: failed to login.')
            node_quit(handler)
            sys.exit(3)

        if action == 'get':
            config = config_get(handler, end_before)
            if config in [False, None]:
                print('ERROR: failed to retrieve config.')
                node_quit(handler)
                sys.exit(4)

            try:
                fh = open(filename, 'a')
                fh.write(config)
                fh.close()
            except:
                print('ERROR: cannot write config to file.')

        elif action == 'put':
            rc = config_put(handler, end_before, config)
            if rc != True:
                print('ERROR: failed to push config.')
                node_quit(handler)
                sys.exit(4)

            # Remove lock file
            lock = '%s/.lock' %(os.path.dirname(filename))

            if os.path.exists(lock):
                os.remove(lock)

            # Mark as configured
            configured = '%s/.configured' %(os.path.dirname(filename))
            if not os.path.exists(configured):
                open(configured, 'a').close()

        node_quit(handler)

    except Exception as e:
        print('ERROR: got an exception')
        print(type(e))  # the exception instance
        print(e.args)   # arguments stored in .args
        print(e)        # __str__ allows args to be printed directly,
        node_quit(handler)
        sys.exit(127)

if __name__ == "__main__":
    main()
    sys.exit(0)
