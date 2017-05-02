#!/usr/bin/env python3
""" Preconfigure vyos node """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

DEBUG = True
TIMEOUT = 180
PASSWORD = 'UNetLabv2!'

import multiprocessing, pexpect, sys, time

def main():
    c = pexpect.spawnu('telnet 127.0.0.1 5023')
    if DEBUG:
        c.logfile = sys.stdout
    i = -1
    while i == -1:
        try:
            i = c.expect(['vyos login:'], timeout = 15)
        except:
            c.sendline('')
            i = -1

    c.sendline('vyos')
    c.expect('Password:', timeout = None)
    c.sendline('vyos')
    c.expect('$', timeout = None)
    c.sendline('install image')
    c.expect('Would you like to continue', timeout = None)
    c.sendline('')
    c.expect('Partition', timeout = None)
    c.sendline('')
    c.expect('Install the image on', timeout = None)
    c.sendline('')
    c.expect('Continue', timeout = None)
    c.sendline('Yes')
    c.expect('How big of a root partition should I create', timeout = None)
    c.sendline('')
    c.expect('What would you like to name this image', timeout = None)
    c.sendline('')
    c.expect('Which one should I copy to', timeout = None)
    c.sendline('')
    c.expect('Enter password for user', timeout = None)
    c.sendline(PASSWORD)
    c.expect('Retype password for user', timeout = None)
    c.sendline(PASSWORD)
    c.expect('Which drive should GRUB modify the boot partition on', timeout = None)
    c.sendline('')
    c.expect('$', timeout = None)
    c.sendline('reboot')
    c.expect('Proceed with reboot', timeout = None)
    c.sendline('Yes')
    c.expect('vyos login:', timeout = None)
    c.sendline('vyos')
    c.expect('Password:', timeout = None)
    c.sendline(PASSWORD)
    c.expect('$', timeout = None)
    c.sendline('configure')
    c.expect('#', timeout = None)
    c.sendline('set interfaces ethernet eth0 description "MANAGEMENT"')
    c.expect('#', timeout = None)
    c.sendline('set interfaces ethernet eth0 address "192.0.2.254/24"')
    c.expect('#', timeout = None)
    c.sendline('commit')
    c.expect('#', timeout = None)
    c.sendline('save')
    c.expect('#', timeout = None)
    c.sendline('exit')
    c.expect('$', timeout = None)
    c.sendline('poweroff')
    c.expect('Proceed with poweroff', timeout = None)
    c.sendline('Yes')

if __name__ == "__main__":
    p = multiprocessing.Process(target = main)
    p.start()
    p.join(TIMEOUT)
    if p.is_alive():
        p.terminate()
        p.join()
        sys.stderr.write("ERROR: preconfiguration failed (timeout)\n")
        sys.exit(1)

