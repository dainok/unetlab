#!/usr/bin/env python3
""" Database structure """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from app import db
import hashlib

roles_to_users = db.Table(
    'roles_to_users',
    db.Column('role', db.String(255), db.ForeignKey('roles.role')),
    db.Column('username', db.String(255), db.ForeignKey('users.username')),
)

class ActiveNode(db.Model):
    __tablename__ = 'active_nodes'
    username = db.Column(db.String(255), db.ForeignKey('users.username'), primary_key = True)
    lab_id = db.Column(db.String(255), db.ForeignKey('labs.id'), primary_key = True)
    node_id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    state = db.Column(db.String(255))
    label = db.Column(db.Integer, unique = True)
    def __repr__(self):
        return '<ActiveNode(lab_id={},node_id={})>'.format(self.lab_id, self.node_id)

class ActiveTopology(db.Model):
    __tablename__ = 'active_topologies'
    username = db.Column(db.String(255), db.ForeignKey('users.username'), db.ForeignKey('users.username'))
    lab_id = db.Column(db.String(255), db.ForeignKey('users.username'), db.ForeignKey('labs.id'))
    src_id = db.Column(db.Integer, db.ForeignKey('active_nodes.label'), primary_key = True)
    src_if = db.Column(db.Integer)
    dst_id = db.Column(db.Integer, db.ForeignKey('active_nodes.label'), primary_key = True)
    dst_if = db.Column(db.Integer)
    def __repr__(self):
        return '<Topology(src_id={}:{},dst_id={}:{}>'.format(self.src_id, self_src_if, self.dst_id, self.dst_if)

class Controller(db.Model):
    __tablename__ = 'controllers'
    id = db.Column(db.String(255), primary_key = True)
    inside_ip = db.Column(db.String(255))
    outside_ip = db.Column(db.String(255))
    master = db.Column(db.Boolean)
    def __repr__(self):
        return '<Controller(id={})>'.format(self.id)

class Lab(db.Model):
    __tablename__ = 'labs'
    id = db.Column(db.String(255), primary_key = True)
    name = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    path = db.Column(db.String(255))
    def __repr__(self):
        return '<Lab(id={})>'.format(self.id)

class Role(db.Model):
    __tablename__ = 'roles'
    role = db.Column(db.String(255), primary_key = True)
    access_to = db.Column(db.String(255))
    can_write = db.Column(db.Boolean())
    users = db.relationship('User', secondary = roles_to_users, back_populates = 'roles')
    def __repr__(self):
        return '<Role({})>'.format(self.role)

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(255), primary_key = True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    labels = db.Column(db.Integer)
    roles = db.relationship('Role', secondary = roles_to_users, back_populates = 'users')
    def __repr__(self):
        return '<User({})>'.format(self.username)

try:
    # Creating database structure
    db.create_all()
except Exception as err:
    # Cannot add tables
    sys.stderr.write('Cannot add tables to database\n')
    sys.exit(1)

# Adding admin role if not exist
role = Role.query.get('admin')
if not role:
    role = Role(
        role = 'admin',
        access_to = '*',
        can_write = True
    )
    db.session.add(role)
    db.session.commit()

# Adding admin user if not exists
user = User.query.get('admin')
if not user:
    user = User(
        username = 'admin',
        password = hashlib.sha256('admin'.encode('utf-8')).hexdigest(),
        name = 'Default Administrator',
        email = 'admin@example.com',
        labels = -1,
        roles = [Role.query.get('admin')]
    )
    db.session.add(user)
    db.session.commit()

