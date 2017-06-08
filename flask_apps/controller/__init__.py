#!/usr/bin/env python3
""" App init """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

""" API
    Methods:
    - GET /api/objects - Retrieves a list of objects
    - GET /api/objects/1 - Retrieves a specific objects
    - POST /api/objects - Creates a new object
    - PUT /api/objects/1 - Edits a specific object
    - DELETE /api/objects/1 - Deletes a specific object
    Return codes:
    - 200 success - Request ok
    - 201 success - New objects has been created
    - 400 bad request - Input request not valid
    - 401 unauthorized - User not authenticated
    - 403 forbidden - User authenticated but not authorized
    - 404 fail - Url or object not found
    - 405 fail - Method not allowed
    - 406 fail - Not acceptable
    - 409 fail - Object already exists, cannot create another one
    - 422 fail - Input data missing or not valid
    - 500 error - Server error, maybe a bug/exception or a backend/database error
"""

import hashlib, memcache, os, sh, shutil, socket, sys
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_script import Command, Manager
from celery import Celery
from controller.config import *

class runCelery(Command):
    def run(self):
        celery.worker_main(['controller.worker', '--loglevel=INFO'])

def make_celery(app):
    celery = Celery(app.import_name, backend = app.config['CELERY_RESULT_BACKEND'], broker = app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

# Loading configuration from file
if not os.path.isdir('/data/etc'):
    try:
        os.makedirs('/data/etc')
    except Exception as err:
        # Cannot create etc directory
        sys.stderr.write('Cannot create "/data/etc" directory ({})\n'.format(err))
        sys.exit(1)
config_file = '/data/etc/controller.ini'
config = loadConfig(config_file)
config_files = [ config_file ]

# Creating the Flask app
app = Flask(__name__)
app_root = os.path.dirname(os.path.abspath(__file__))
app.config.update(
    BUNDLE_ERRORS = True,
    DEBUG = config['app']['debug'],
    TESTING = config['app']['testing'],
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    SQLALCHEMY_DATABASE_URI = config['app']['database_uri'],
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)
api = Api(app)
db = SQLAlchemy(app)
cache = memcache.Client([config['app']['memcache_server']], debug = 0)
celery = make_celery(app)
api_key = config['app']['api_key']
manager = Manager(app)
manager.add_command('runcelery', runCelery())
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
        access_to = '.*',
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

# Adding local repository if not present
if not os.path.isdir('{}/local'.format(config['app']['lab_repository'])):
    try:
        os.makedirs('{}/local'.format(config['app']['lab_repository']))
        sh.git('-C', '{}/local'.format(config['app']['lab_repository']), 'init', '-q', _bg = False)
    except Exception as err:
        # Cannot create local reporitory
        shutil.rmtree('{}'.format(config['app']['lab_repository']), ignore_errors = True)
        sys.stderr.write('Cannot create local repository ({})\n'.format(err))
        sys.exit(1)
repository = RepositoryTable.query.get('local')
if not repository:
    repository = RepositoryTable(
        id = 'local'
    )
    db.session.add(repository)
    db.session.commit()

# Adding first controller if not present
router = RouterTable.query.get(0)
if not router:
    router = RouterTable(
        id = 0,
        inside_ip = '127.0.0.1',
        outside_ip = '127.0.0.1'
    )
    db.session.add(router)
    db.session.commit()

@app.errorhandler(404)
def http_404(err):
    response = {
        'message': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'
    }
    return json.dumps(response, indent = 4, sort_keys = True) + '\n', 404
# TODO 400 401 403 405 409 422 500 

# Routing
api.add_resource(Auth, '/api/v1/auth')
api.add_resource(BootstrapNode, '/api/v1/bootstrap/nodes/<int:label>')
api.add_resource(BootstrapRouter, '/api/v1/bootstrap/routers/<int:router_id>')
api.add_resource(Lab, '/api/v1/labs', '/api/v1/labs/<string:lab_id>')
api.add_resource(Node, '/api/v1/nodes', '/api/v1/nodes/<int:label>/<string:action>')
api.add_resource(Repository, '/api/v1/repositories', '/api/v1/repositories/<string:repository_id>')
api.add_resource(Role, '/api/v1/roles', '/api/v1/roles/<string:role>')
api.add_resource(Router, '/api/v1/routers', '/api/v1/routers/<int:router_id>')
api.add_resource(Routing, '/api/v1/routing')
api.add_resource(Task, '/api/v1/tasks', '/api/v1/tasks/<string:task_id>')
api.add_resource(User, '/api/v1/users', '/api/v1/users/<string:username>')

