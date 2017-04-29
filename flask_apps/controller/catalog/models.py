#!/usr/bin/env python3
""" Database structure """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170429'

from controller import db

roles_to_users = db.Table(
    'roles_to_users',
    db.Column('role', db.String(128), db.ForeignKey('roles.role')),
    db.Column('username', db.String(128), db.ForeignKey('users.username')),
)

class ActiveLabTable(db.Model):
    __tablename__ = 'active_labs'
    __mapper_args__ = {'confirm_deleted_rows': False}
    instance = db.Column(db.String(128), unique = True, nullable = False)
    id = db.Column(db.String(128), primary_key = True)
    username = db.Column(db.String(128), db.ForeignKey('users.username'), primary_key = True)
    author = db.Column(db.String(128))
    name = db.Column(db.String(128))
    version = db.Column(db.Integer)
    json = db.Column(db.Text)
    repository_id = db.Column(db.String(128), db.ForeignKey('repositories.id'))
    nodes = db.relationship('ActiveNodeTable', cascade = 'save-update, merge, delete')

    def __repr__(self):
        return '<ActiveLab(id={},username={})>'.format(self.id, self.username)

class ActiveNodeTable(db.Model):
    __tablename__ = 'active_nodes'
    __mapper_args__ = {'confirm_deleted_rows': False}
    instance = db.Column(db.String(128), db.ForeignKey('active_labs.instance'))
    node_id = db.Column(db.Integer)
    controller_id = db.Column(db.Integer)
    state = db.Column(db.String(128))
    label = db.Column(db.Integer, primary_key = True, autoincrement = False)
    interfaces = db.relationship('ActiveInterfaceTable', cascade = 'save-update, merge, delete')

    def __repr__(self):
        return '<ActiveNode(instance={},node_id={})>'.format(self.instance, self.node_id)

class ActiveInterfaceTable(db.Model):
    __tablename__ = 'active_interfaces'
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    label = db.Column(db.Integer, db.ForeignKey('active_nodes.label'), primary_key = True, autoincrement = False)
    dst_label = db.Column(db.Integer)
    dst_if = db.Column(db.Integer)

    def __repr__(self):
        return '<ActiveInterfaceTable(id={})>'.format(self.id)

class ControllerTable(db.Model):
    __tablename__ = 'controllers'
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    inside_ip = db.Column(db.String(128))
    outside_ip = db.Column(db.String(128))
    master = db.Column(db.Boolean)

    def __repr__(self):
        return '<Controller(id={})>'.format(self.id)

class LabTable(db.Model):
    __tablename__ = 'labs'
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = db.Column(db.String(128), primary_key = True)
    author = db.Column(db.String(128))
    name = db.Column(db.String(128))
    version = db.Column(db.Integer)
    json = db.Column(db.Text)
    repository_id = db.Column(db.String(128), db.ForeignKey('repositories.id'))

    def __repr__(self):
        return '<Lab(id={})>'.format(self.id)

class RepositoryTable(db.Model):
    __tablename__ = 'repositories'
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = db.Column(db.String(128), primary_key = True)
    url = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    labs = db.relationship('LabTable', cascade = 'save-update, merge, delete')
    active_labs = db.relationship('ActiveLabTable', cascade = 'save-update, merge, delete')

    def __repr__(self):
        return '<Repository(repository={})>'.format(self.repository)

class RoleTable(db.Model):
    __tablename__ = 'roles'
    __mapper_args__ = {'confirm_deleted_rows': False}
    role = db.Column(db.String(128), primary_key = True)
    access_to = db.Column(db.String(128))
    can_write = db.Column(db.Boolean())
    users = db.relationship('UserTable', secondary = roles_to_users, back_populates = 'roles')

    def __repr__(self):
        return '<Role(role={})>'.format(self.role)

class TaskTable(db.Model):
    __tablename__ = 'tasks'
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = db.Column(db.String(128), primary_key = True)
    status = db.Column(db.String(128))
    message = db.Column(db.Text)
    progress = db.Column(db.Integer)
    username = db.Column(db.String(128), db.ForeignKey('users.username'), db.ForeignKey('users.username'))

    def __repr__(self):
        return '<Task(id={})>'.format(self.id)

class UserTable(db.Model):
    __tablename__ = 'users'
    __mapper_args__ = {'confirm_deleted_rows': False}
    username = db.Column(db.String(128), primary_key = True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique = True)
    labels = db.Column(db.Integer)
    roles = db.relationship('RoleTable', secondary = roles_to_users, back_populates = 'users')
    tasks = db.relationship('TaskTable', cascade = 'save-update, merge, delete')
    active_labs = db.relationship('ActiveLabTable', cascade = 'save-update, merge, delete')

    def __repr__(self):
        return '<User(username={})>'.format(self.username)

