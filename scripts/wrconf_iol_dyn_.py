#!/usr/bin/env python3

# scripts/wrconf_iol_dyn_.py
#
# Auto config write for iol and dynamis on export
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
# @copyright 2014-2016 Andrea Dainese
# @license http://www.gnu.org/licenses/gpl.html
# @link http://www.unetlab.com/
# @version 20160114

import getopt, multiprocessing, os, pexpect, re, sys, time

username = 'cisco'
password = 'cisco'
secret = 'cisco'
conntimeout = 3     # Maximum time for console connection
expctimeout = 3     # Maximum time for each short expect
longtimeout = 30    # Maximum time for each long expect
timeout = 60        # Maximum run time (conntimeout is included)

def node_login(handler):
    # Send an empty line, and wait for the login prompt
    i = -1
    while i == -1:
        try:
            handler.sendline('\r\n')
            i = handler.expect([
                'Username:',
                '\(config',
                '>',
                '#',
                'Would you like to enter the'], timeout = 5)
        except:
            i = -1

    if i == 0:
        # Need to send username and password
        handler.sendline(username)
        try:
            handler.expect('Password:', timeout = expctimeout)
        except:
            print('ERROR: error waiting for "Password:" prompt.')
            node_quit(handler)
            return False

        handler.sendline(password)
        try:
            j = handler.expect(['>', '#'], timeout = expctimeout)
        except:
            print('ERROR: error waiting for [">", "#"] prompt.')
            node_quit(handler)
            return False

        if j == 0:
            # Secret password required
            handler.sendline(secret)
            try:
                handler.expect('#', timeout = expctimeout)
            except:
                print('ERROR: error waiting for "#" prompt.')
                node_quit(handler)
                return False
            return True
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
        try:
            handler.expect('#', timeout = expctimeout)
        except:
            print('ERROR: error waiting for "#" prompt.')
            node_quit(handler)
            return False
        return True
    elif i == 2:
        # Need higher privilege
        handler.sendline('enable')
        try:
            j = handler.expect(['Password:', '#'])
        except:
            print('ERROR: error waiting for ["Password:", "#"] prompt.')
            node_quit(handler)
            return False
        if j == 0:
            # Need do provide secret
            handler.sendline(secret)
            try:
                handler.expect('#', timeout = expctimeout)
            except:
                print('ERROR: error waiting for "#" prompt.')
                node_quit(handler)
                return False
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
    elif i == 4:
        # First boot detected
        handler.sendline('no')
        try:
            handler.expect('Press RETURN to get started', timeout = longtimeout)
        except:
            print('ERROR: error waiting for "Press RETURN to get started" prompt.')
            node_quit(handler)
            return False
        handler.sendline('\r\n')
        try:
            handler.expect('Router>', timeout = expctimeout)
        except:
            print('ERROR: error waiting for "Router> prompt.')
            node_quit(handler)
            return False
        handler.sendline('enable')
        try:
            handler.expect('Router#', timeout = expctimeout)
        except:
            print('ERROR: error waiting for "Router# prompt.')
            node_quit(handler)
            return False
        return True
    else:
        # Unexpected output
        node_quit(handler)
        return False

def node_quit(handler):
    if handler.isalive() == True:
        handler.sendline('quit\n')
    handler.close()

def config_write(handler):
    # Clearing all "expect" buffer
    while True:
        try:
            handler.expect('#', timeout = 0.1)
        except:
            break

    # Disable paging
    handler.sendline('terminal length 0')
    try:
        handler.expect('#', timeout = expctimeout)
    except:
        print('ERROR: error waiting for "#" prompt.')
        node_quit(handler)
        return False

    # Getting the config
    handler.sendline('write\n')
    try:
        handler.expect('#', timeout = longtimeout)
    except:
        print('ERROR: error waiting for "#" prompt.')
        node_quit(handler)
        return False
    return True

def usage():
    print('Usage: %s <standard options>' %(sys.argv[0]));
    print('Standard Options:');
    print('-p <n>    *Console port');
    print('-t <n>     Timeout (default = %i)' %(timeout));
    print('* Mandatory option')

def now():
    # Return current UNIX time in milliseconds
    return int(round(time.time() * 1000))

def main(port):
    try:
        # Connect to the device
        tmp = conntimeout
        while (tmp > 0):
            handler = pexpect.spawn('telnet 127.0.0.1 %i' %(port))
            time.sleep(0.1)
            tmp = tmp - 0.1
            if handler.isalive() == True:
                break

        if (handler.isalive() != True):
            print('ERROR: cannot connect to port "%i".' %(port))
            node_quit(handler)
            sys.exit(1)

        rc = node_login(handler)
        if rc != True:
           print('ERROR: failed to login.')
           node_quit(handler)
           sys.exit(1)
        wr = config_write(handler)
        if wr in [False, None]:
           print('ERROR: failed to write config.')
           node_quit(handler)
           sys.exit(1)

        node_quit(handler)
        sys.exit(0)

    except Exception as e:
        print('ERROR: got an exception')
        print(type(e))  # the exception instance
        print(e.args)   # arguments stored in .args
        print(e)        # __str__ allows args to be printed directly,
        node_quit(handler)
        return False

if __name__ == "__main__":
    action = None
    filename = None
    port = None

    # Getting parameters from command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:t:', ['port=', 'timeout='])
    except getopt.GetoptError as e:
        usage()
        sys.exit(3)

    for o, a in opts:
        if o in ('-p', '--port'):
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
    if port == None :
        usage()
        print('ERROR: missing mandatory parameter.')
        sys.exit(1)
    if timeout < 0:
        usage()
        print('ERROR: timeout must be 0 or higher.')
        sys.exit(1)
    if port < 0:
        usage()
        print('ERROR: port must be 32768 or higher.')
        sys.exit(1)
    
    # Backgrounding the script
    end_before = now() + timeout
    p = multiprocessing.Process(target=main, name="Main", args=(port,))
    p.start()

    while (p.is_alive() and now() < end_before):
        # Waiting for the child process to end
        time.sleep(1)

    if p.is_alive():
        # Timeout occurred
        print('ERROR: timeout occurred.')
        p.terminate()
        sys.exit(127)

    if p.exitcode != 0:
        sys.exit(127)

    sys.exit(0)
