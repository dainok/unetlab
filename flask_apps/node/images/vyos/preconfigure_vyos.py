#!/usr/bin/env python3
""" Preconfigure vyos node """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

DEBUG = True
TIMEOUT = 120
PASSWORD = 'UNetLabv2!'

import multiprocessing, pexpect, sys, time

def main():
    p = pexpect.spawnu('telnet 127.0.0.1 5023')
    if DEBUG:
        p.logfile = sys.stdout
    i = -1
    while i == -1:
        try:
            i = p.expect(['vyos login:'], timeout = 15)
        except:
            p.sendline('')
            i = -1

    p.sendline('vyos')
    p.expect('Password:')
    p.sendline('vyos')
    p.expect('$')
    p.sendline('install image')
    p.expect('Would you like to continue')
    p.sendline('')
    p.expect('Partition')
    p.sendline('')
    p.expect('Install the image on')
    p.sendline('')
    p.expect('Continue')
    p.sendline('Yes')
    p.expect('How big of a root partition should I create')
    p.sendline('')
    p.expect('What would you like to name this image')
    p.sendline('')
    p.expect('Which one should I copy to sda')
    p.sendline('')
    p.expect('Enter password for user')
    p.sendline(PASSWORD)
    p.expect('Retype password for user')
    p.sendline(PASSWORD)
    p.expect('Which drive should GRUB modify the boot partition on')
    p.sendline('')
    p.expect('$')
    p.sendline('poweroff')
    p.expect('Proceed with poweroff')
    p.sendline('Yes')

if __name__ == "__main__":
    p = multiprocessing.Process(target = main)
    p.start()
    p.join(TIMEOUT)
    if p.is_alive():
        p.terminate()
        p.join()
        sys.stderr.write("ERROR: preconfiguration failed (timeout)\n")
        sys.exit(1)
