#!/usr/bin/env python3
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
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.restful import Api, Resource
from config import *
from models import *

# Loading configuration from file
config_file = '/data/etc/controller.ini'
config = loadConfig(config_file)
config_files = [ config_file ]

# Creating the Flask app
app = Flask(__name__)
app.config.update(
    DEBUG = config['app']['debug'],
    TESTING = config['app']['testing'],
    SQLALCHEMY_DATABASE_URI = config['app']['database_uri']
)
api = Api(app)
db = SQLAlchemy(app)

#api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')

@app.route('/api/users', methods = ['GET'])
def apiUsers():
    return User.query.get_or_404('username')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = config['app']['port'], extra_files = config_files)

