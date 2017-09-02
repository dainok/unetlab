#!/usr/bin/env python3
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import configparser, os, random, sys

def loadConfig(config_file):
    if not os.path.isfile(config_file):
        # File is not present
        try:
            # Write an empty file
            open(config_file, 'a').close()
        except Exception as err:
            # Cannot write configuration file
            sys.stderr.write('Cannot create configuration file "{}"\n'.format(config_file))
            sys.exit(1)

    # Loading Config
    config = configparser.ConfigParser()
    need_to_save = False
    try:
        # Loading configuration file
        config.read(config_file)
    except Exception as err:
        # Cannot load configuration file
        sys.stderr.write('Cannot load configuration file "{}"\n'.format(config_file))
        sys.exit(1)

    # Setting default values
    if not config.has_section('app'):
        config.add_section('app')
        need_to_save = True
    if not config.has_section('advanced'):
        config.add_section('advanced')
        need_to_save = True
    if not config.has_option('app', 'api_key'):
        api_key = os.environ.get('API')
        if not api_key:
            api_key = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for c in range(40))
        config['app']['api_key'] = api_key
        need_to_save = True
    if not config.has_option('app', 'database_uri'):
        config['app']['database_uri'] = 'mysql://unetlab:UNetLabv2!@localhost/unetlab'
        need_to_save = True
    if not config.has_option('app', 'memcache_server'):
        config['app']['memcache_server'] = '127.0.0.1:11211'
        need_to_save = True
    if not config.has_option('app', 'debug'):
        config['app']['debug'] = 'False'
        need_to_save = True
    if not config.has_option('app', 'port'):
        config['app']['port'] = '5000'
        need_to_save = True
    if not config.has_option('app', 'testing'):
        config['app']['testing'] = 'False'
        need_to_save = True
    if not config.has_option('app', 'lab_extension'):
        config['app']['lab_extension'] = 'junl'
        need_to_save = True
    if not config.has_option('app', 'lab_repository'):
        config['app']['lab_repository'] = '/data/repositories'
        need_to_save = True
    if not config.has_option('app', 'inside_ip'):
        config['app']['inside_ip'] = '172.16.0.2'
        need_to_save = True
    if not config.has_option('app', 'outside_ip'):
        config['app']['outside_ip'] = '0.0.0.0'
        need_to_save = True
    if not config.has_option('advanced', 'label_length'):
        config['advanced']['label_length'] = '2'
        need_to_save = True
    if not config.has_option('advanced', 'interface_length'):
        config['advanced']['interface_length'] = '1'
        need_to_save = True
    if not config.has_option('advanced', 'controller_length'):
        config['advanced']['controller_length'] = '1'
        need_to_save = True
    if not config.has_option('advanced', 'controller_port'):
        config['advanced']['controller_port'] = '5005'
        need_to_save = True

    if need_to_save:
        # Need to update configuration file
        try:
            with open(config_file, 'w') as config_fd:
                config.write(config_fd)
                config_fd.close()
        except Exception as err:
            # Cannot update configuration file
            sys.stderr.write('Cannot update configuration file "{}"\n'.format(config_file))
            sys.exit(1)

    # Parsing
    result = config._sections
    result['app']['debug'] = config.getboolean('app', 'debug')
    result['app']['port'] = config.getint('app', 'port')
    result['app']['testing'] = config.getboolean('app', 'testing')
    result['advanced']['controller_port'] = config.getint('advanced', 'controller_port')
    result['advanced']['label_length'] = config.getint('advanced', 'label_length')
    result['advanced']['interface_length'] = config.getint('advanced', 'interface_length')
    result['advanced']['controller_length'] = config.getint('advanced', 'controller_length')

    return result
