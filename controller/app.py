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
from flask_restful import Api, Resource
from config import *
from models import *
from parsers import *

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
    SQLALCHEMY_DATABASE_URI = config['app']['database_uri']
)
api = Api(app)
db = SQLAlchemy(app)

class User(Resource):
    def get(self, username = None, page = 1):
        if not username:
            # List all users
            users = UserTable.query.paginate(page, 10).items
        else:
            # List a single user if exists, else 404
            users = [ UserTable.query.get_or_404(username) ]
        data = {}
        for user in users:
            # Print each user and roles
            data[user.username] = {
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'labels': user.labels,
                'roles': []
            }
            for role in user.roles:
                data[user.username]['roles'].append(role.role)
        return {
            'status': 'success',
            'data': data
        }
    def post(self):
        args = user_parser.parse_args(strict=True)
        user = {
            'username': args['username'],
            'password': args['password'],
            'name': args['name'],
            'email': args['email'],
            'labels': args['labels'],
            'roles': args['roles']
        }
        return {
            'status': 'success',
        }

        
        

api.add_resource(User, '/api/v1/users', '/api/v1/users/<string:username>')


#@app.route('/api/users', methods = ['GET'])
#def apiUsers():
#    return User.query.get_or_404('username')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = config['app']['port'], extra_files = config_files)

