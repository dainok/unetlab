#!/usr/bin/env python3
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'


def loadConfig(config_file):
    import configparser, os, sys

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
    if not config.has_section('controller'):
        config.add_section('controller')
        need_to_save = True
    if not config.has_section('advanced'):
        config.add_section('advanced')
        need_to_save = True
    if not config.has_option('app', 'database_uri'):
        config['app']['database_uri'] = 'mysql://root:unetlab@localhost/unetlab'
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
        config['app']['lab_extension'] = 'unl'
        need_to_save = True
    if not config.has_option('app', 'lab_repository'):
        config['app']['lab_repository'] = '/data/labs'
        need_to_save = True
    if not config.has_option('controller', 'id'):
        config['controller']['id'] = '0'
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
    result['controller']['id'] = config.getint('controller', 'id')
    result['advanced']['label_length'] = config.getint('advanced', 'label_length')
    result['advanced']['interface_length'] = config.getint('advanced', 'interface_length')
    result['advanced']['controller_length'] = config.getint('advanced', 'controller_length')

    return result

