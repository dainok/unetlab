#!/usr/bin/env python3

# scripts/config_xrv.py
#
# Import/Export script for vIOS.
#
# @author Andrea Dainese <andrea.dainese@gmail.com>
# @copyright 2014-2016 Andrea Dainese
# @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
# @link http://www.unetlab.com/
# @version 20160719

import getopt, multiprocessing, os, pexpect, re, sys, time, platform


username = 'admin'
password = ''
conntimeout = 3     # Maximum time for console connection
expctimeout = 10     # Maximum time for each short expect
longtimeout = 30    # Maximum time for each long expect
timeout = 60        # Maximum run time (conntimeout is included)
ip = '127.0.0.1'
MTK_PROMPT = '\]\s> '

def node_login(handler):
    # Send an empty line, and wait for the login prompt
    i = -1
    while i == -1:
        try:
            handler.send('\r\n')
            i = handler.expect([
                'Login: ',
                MTK_PROMPT], timeout = 5)            
        except:
            i = -1

    if i == 0:
        # Need to send username and password
        handler.send(username + '+c512wt\r\n')
        try:
            handler.expect('Password:', timeout = expctimeout)
        except:
            print('ERROR: error waiting for "Password:" prompt.')
            node_quit(handler)
            return False

        handler.send(password+'\r\n')
        handler.send('\r\n')
        try:
            handler.expect(MTK_PROMPT, timeout = expctimeout)
        except:
            print('ERROR: error waiting for "%s" prompt.' %(MTK_PROMPT))
            node_quit(handler)
            return False
        return True        
    if i == 1:
        #Already logged in on serial console
        return True
    else:
        # Unexpected output
        node_quit(handler)
        return False

def node_quit(handler):    
    if handler.isalive() == True:
        handler.send('/quit\r\n')
    handler.close()

def config_get(handler):
    # Clearing all "expect" buffer
    while True:
        try:
            handler.send('\r\n')
            handler.expect(MTK_PROMPT, timeout = expctimeout)
            break
        except:
            continue

    # Getting the config
    handler.send('/export\r\n')
    try:
        handler.expect(MTK_PROMPT, timeout = longtimeout)
    except:
        print('ERROR: error waiting for "end" marker.')
        node_quit(handler)
        return False
    
    config = ''
    try:
        config = handler.before.decode()
    except:
        config = handler.before        

    # Manipulating the config
    config = re.sub('\r', '', config, flags=re.DOTALL)                                      # Unix style
    config = re.sub('/export', '\r', config, flags=re.DOTALL)                                      # Unix style
    config = re.sub('.*!! IOS XR Configuration', '!! IOS XR Configuration', config, flags=re.DOTALL)   # Header
    config = re.sub('no logging console' , '\n!\n' , config, flags=re.DOTALL) # suppress no login console
    config = re.sub('$.*', '\n!\nend\n', config, flags=re.DOTALL)                # Footer
    return config

def config_put(handler): 
    while True:
        try:
           i = handler.expect('CVAC-4-CONFIG_DONE', timeout)
        except:
           return False
        return True

def usage():
    print('Usage: %s <standard options>' %(sys.argv[0]));
    print('Standard Options:');
    print('-a <s>    *Action can be:')
    print('           - get: get the startup-configuration and push it to a file')
    print('           - put: put the file as startup-configuration')
    print('-f <s>    *File');
    print('-p <n>    *Console port');
    print('-t <n>     Timeout (default = %i)' %(timeout));
    print('* Mandatory option')

def now():
    # Return current UNIX time in milliseconds
    return int(round(time.time() * 1000))

def qqq(action, fiename, port):
    try:
        # Connect to the device
        tmp = conntimeout
        handler = pexpect.spawnu('telnet %s %i' %(ip, port), maxread=20000)
        handler.logfile = sys.stdout        
        handler.crlf = '\r\n'
        while (tmp > 0):            
            #handler.sendline('')
            time.sleep(0.1)
            tmp = tmp - 0.1
            if handler.isalive() == True:
                break

        if action == 'get':
            if (handler.isalive() != True):
                print('ERROR: cannot connect to port "%i".' %(port))
                node_quit(handler)
                sys.exit(1)
            rc = node_login(handler)
            if rc != True:
                print('ERROR: failed to login.')
                node_quit(handler)
                sys.exit(1)
            config = config_get(handler)
            if config in [False, None]:
                print('ERROR: failed to retrieve config.')
                node_quit(handler)
                sys.exit(1)

            try:
                fd = open(filename, 'a')
                fd.write(config)
                fd.close()
            except:
                print('ERROR: cannot write config to file.')
                node_quit(handler)
                sys.exit(1)
        elif action == 'put':
            rc = config_put(handler)
            if rc != True:
                print('ERROR: failed to push config.')
                node_quit(handler)
                sys.exit(1)

            # Remove lock file
            lock = '%s/.lock' %(os.path.dirname(filename))

            if os.path.exists(lock):
                os.remove(lock)

            # Mark as configured
            configured = '%s/.configured' %(os.path.dirname(filename))
            if not os.path.exists(configured):
                open(configured, 'a').close()

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
        opts, args = getopt.getopt(sys.argv[1:], 'a:p:t:f:i', ['action=', 'port=', 'timeout=', 'file=', 'address='])
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
                timeout = int(a)
            except:
                timeout = -1
        elif o in ('-i', '--address'):
            ip = a
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
            fd = open(filename, 'r')
            config = fd.read()
            fd.close()
        except:
            usage()
            print('ERROR: cannot read from file.')
            sys.exit(1)

    qqq('get','/tmp/unl_cfg_2_dh1voc',port)
    # Backgrounding the script
#    end_before = now() + timeout * 1000
 #   p = multiprocessing.Process(target=main, name="Main", args=(action, filename, port))
#    p.start()

#    while (p.is_alive() and now() < end_before):
        # Waiting for the child process to end
 #       time.sleep(1)

#    if p.is_alive():q
        # Timeout occurred
#        print('ERROR: timeout occurred.')
#        p.terminate()
#        sys.exit(127)

#    if p.exitcode != 0:
#        sys.exit(127)

    sys.exit(0)
