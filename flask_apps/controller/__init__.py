#!/usr/bin/env python3
""" App init """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

import sys
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from controller.config import *

# Loading configuration from file
config_file = '/data/etc/controller.ini'
config = loadConfig(config_file)
config_files = [ config_file ]

# Creating the Flask app
app = Flask(__name__)
app.config.update(
    BUNDLE_ERRORS = True,
    DEBUG = config['app']['debug'],
    TESTING = config['app']['testing'],
    SQLALCHEMY_DATABASE_URI = config['app']['database_uri'],
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)
api = Api(app)
db = SQLAlchemy(app)
manager = Manager(app)
#TODO manager.add_command('db', MigrateCommand)

# Postpone to avoid circular import
from controller.catalog.resources import *
from controller.catalog.models import *

try:
    # Creating database structure
    db.create_all()
except (RuntimeError, TypeError, NameError):
    # Cannot add tables
    sys.stderr.write('Cannot add tables to database\n')
    sys.exit(1)

# Adding admin role if not exist
role = RoleTable.query.get('admin')
if not role:
    role = RoleTable(
        role = 'admin',
        access_to = '*',
        can_write = True
    )
    db.session.add(role)
    db.session.commit()

# Adding admin user if not exists
user = UserTable.query.get('admin')
if not user:
    user = UserTable(
        username = 'admin',
        password = hashlib.sha256('admin'.encode('utf-8')).hexdigest(),
        name = 'Default Administrator',
        email = 'admin@example.com',
        labels = -1,
        roles = [RoleTable.query.get('admin')]
    )
    db.session.add(user)
    db.session.commit()

# Routing
api.add_resource(User, '/api/v1/users', '/api/v1/users/<string:username>')
