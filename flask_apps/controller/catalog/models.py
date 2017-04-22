#!/usr/bin/env python3
""" Database structure """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170403'

from controller import db
import hashlib

roles_to_users = db.Table(
    'roles_to_users',
    db.Column('role', db.String(128), db.ForeignKey('roles.role')),
    db.Column('username', db.String(128), db.ForeignKey('users.username')),
)

class ActiveLabTable(db.Model):
    __tablename__ = 'active_labs'
    id = db.Column(db.String(128), primary_key = True)
    username = db.Column(db.String(128), db.ForeignKey('users.username'), primary_key = True)
    author = db.Column(db.String(128))
    name = db.Column(db.String(128))
    version = db.Column(db.Integer)
    json = db.Column(db.Text)
    repository = db.Column(db.String(128), db.ForeignKey('repositories.repository'))
    # array of avtive nodes

class ActiveNodeTable(db.Model):
    __tablename__ = 'active_nodes'
    username = db.Column(db.String(128), db.ForeignKey('users.username'), primary_key = True)
    lab_id = db.Column(db.String(128), db.ForeignKey('labs.id'), primary_key = True)
    node_id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    state = db.Column(db.String(128))
    label = db.Column(db.Integer, unique = True)

    def __repr__(self):
        return '<ActiveNode(lab_id={},node_id={})>'.format(self.lab_id, self.node_id)

class ActiveTopologyTable(db.Model):
    __tablename__ = 'active_topologies'
    username = db.Column(db.String(128), db.ForeignKey('users.username'), db.ForeignKey('users.username'))
    lab_id = db.Column(db.String(128), db.ForeignKey('users.username'), db.ForeignKey('labs.id'))
    src_id = db.Column(db.Integer, db.ForeignKey('active_nodes.label'), primary_key = True)
    src_if = db.Column(db.Integer)
    dst_id = db.Column(db.Integer, db.ForeignKey('active_nodes.label'), primary_key = True)
    dst_if = db.Column(db.Integer)

    def __repr__(self):
        return '<Topology(src_id={}:{},dst_id={}:{}>'.format(self.src_id, self_src_if, self.dst_id, self.dst_if)

class ControllerTable(db.Model):
    __tablename__ = 'controllers'
    id = db.Column(db.Integer, primary_key = True)
    inside_ip = db.Column(db.String(128))
    outside_ip = db.Column(db.String(128))
    master = db.Column(db.Boolean)

    def __repr__(self):
        return '<Controller(id={})>'.format(self.id)

class LabTable(db.Model):
    __tablename__ = 'labs'
    id = db.Column(db.String(128), primary_key = True)
    author = db.Column(db.String(128))
    name = db.Column(db.String(128))
    version = db.Column(db.Integer)
    json = db.Column(db.Text)
    repository = db.Column(db.String(128), db.ForeignKey('repositories.repository'))

    def __repr__(self):
        return '<Lab(id={})>'.format(self.id)

class RepositoryTable(db.Model):
    __tablename__ = 'repositories'
    repository = db.Column(db.String(128), primary_key = True)
    url = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<Repository(repository={})>'.format(self.repository)

class RoleTable(db.Model):
    __tablename__ = 'roles'
    role = db.Column(db.String(128), primary_key = True)
    access_to = db.Column(db.String(128))
    can_write = db.Column(db.Boolean())
    users = db.relationship('UserTable', secondary = roles_to_users, back_populates = 'roles')

    def __repr__(self):
        return '<Role(role={})>'.format(self.role)

class TaskTable(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.String(128), primary_key = True)
    status = db.Column(db.String(128))
    message = db.Column(db.Text)
    progress = db.Column(db.Integer)
    username = db.Column(db.String(128), db.ForeignKey('users.username'), db.ForeignKey('users.username'))

    def __repr__(self):
        return '<Task(id={})>'.format(self.id)

class UserTable(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(128), primary_key = True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique = True)
    labels = db.Column(db.Integer)
    roles = db.relationship('RoleTable', secondary = roles_to_users, back_populates = 'users')
    active_labs = db.relationship('ActiveLabTable')

    def __repr__(self):
        return '<User(username={})>'.format(self.username)
