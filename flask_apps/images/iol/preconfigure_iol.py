#!/usr/bin/env python3
""" Preconfigure vyos node """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

DEBUG = True
TIMEOUT = 180
PASSWORD = 'UNetLabv2!'

import multiprocessing, os, pexpect, sys, time

def main():
    open('NETMAP', 'a').close()
    c = pexpect.spawnu('./iol.bin 1')
    if DEBUG:
        c.logfile = sys.stdout
    i = -1
    c.expect(['Would you like to enter the initial configuration dialog'], timeout = None)
    c.sendline('no')
    c.expect('Would you like to terminate autoinstall', timeout = None)
    c.sendline('\r\n')
    i = -1
    while i == -1:
        try:
            i = c.expect(['>'], timeout = 5)
        except:
            c.sendline('\r\n')
            i = -1
    c.sendline('enable')
    c.expect('#', timeout = None)
    c.sendline('configure terminal')
    c.expect('#', timeout = None)
    c.sendline('username admin privilege 15 password {}'.format(PASSWORD))
    c.expect('#', timeout = None)
    c.sendline('hostname node')
    c.expect('#', timeout = None)
    c.sendline('ip domain-name example.com')
    c.expect('#', timeout = None)
    c.sendline('crypto key generate rsa')
    c.expect('How many bits in the modulus', timeout = None)
    c.sendline('768')
    c.expect('#', timeout = None)
    c.sendline('ip ssh version 2')
    c.expect('#', timeout = None)
    c.sendline('ip scp server enable')
    c.expect('#', timeout = None)
    c.sendline('line vty 0 4')
    c.expect('#', timeout = None)
    c.sendline('login local')
    c.expect('#', timeout = None)
    c.sendline('transport input ssh')
    c.expect('#', timeout = None)
    c.sendline('interface Ethernet0/0')
    c.expect('#', timeout = None)
    c.sendline('ip address 192.0.2.254 255.255.255.0')
    c.expect('#', timeout = None)
    c.sendline('no shutdown')
    c.expect('#', timeout = None)
    c.sendline('end')
    c.expect('#', timeout = None)
    c.sendline('copy running-config startup-config')
    c.expect('Destination filename', timeout = None)
    c.sendline('\r\n')
    c.expect('#', timeout = None)
    c.close()
    time.sleep(0.5)
    c.close(force = True)
    os.remove('NETMAP')

if __name__ == "__main__":
    p = multiprocessing.Process(target = main)
    p.start()
    p.join(TIMEOUT)
    if p.is_alive():
        p.terminate()
        p.join()
        sys.stderr.write("ERROR: preconfiguration failed (timeout)\n")
        sys.exit(1)

