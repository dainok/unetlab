#!/usr/bin/env python3
""" Resources """
__author__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__copyright__ = 'Andrea Dainese <andrea.dainese@gmail.com>'
__license__ = 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode'
__revision__ = '20170430'

import hashlib, io, json, os, random, shutil, uuid
from flask import abort, request, send_file
from flask_restful import Resource
from sqlalchemy import and_
from controller import app_root, cache, config
from controller.catalog.aaa import checkAuth, checkAuthz, checkAuthzPath
from controller.catalog.models import *
from controller.catalog.parsers import *
from controller.catalog.tasks import *

def activateLab(username, jlab):
    # Checking for available labels
    available_labels = getAvailableLabels(username)
    if available_labels != -1 and available_labels < len(jlab['topology']['nodes']):
        abort(403)
    # Make the lab active
    active_lab = ActiveLabTable(
        id = jlab['id'],
        name = jlab['name'],
        repository_id = jlab['repository'],
        author = jlab['author'],
        version = jlab['version'],
        json = json.dumps(jlab, separators = (',', ':'), sort_keys = True),
        username = username,
        instance = str(uuid.uuid4())
    )
    db.session.add(active_lab)
    db.session.commit()
    # Setting labels
    label = 0
    connections = {}
    for node_id, node in jlab['topology']['nodes'].items():
        while ActiveNodeTable.query.get(label) != None:
            label = label + 1
        active_lab.nodes.append(ActiveNodeTable(
            node_id = node_id,
            state = 'off',
            label = label
        ))
        for interface_id, interface in node['interfaces'].items():
            if 'connection' in interface:
                if not interface['connection'] in connections:
                    connections[interface['connection']] = []
                connections[interface['connection']].append({
                    'node_id': node_id,
                    'label': label,
                    'interface_id': interface_id
                })
    db.session.commit()
    # Setting connections
    for connection_id, connection in connections.items():
        if len(connection) == 2:
            # Evaluating only valid P2P connections
            db.session.add(ActiveInterfaceTable(
                id = connection[0]['interface_id'],
                label = connection[0]['label'],
                dst_label = connection[1]['label'],
                dst_if = connection[1]['interface_id']
            ))
            db.session.add(ActiveInterfaceTable(
                id = connection[1]['interface_id'],
                label = connection[1]['label'],
                dst_label = connection[0]['label'],
                dst_if = connection[0]['interface_id']
            ))
            db.session.commit()

def fixjLab(jlab):
    # Check lab integrity
    if not 'topology' in jlab:
        jlab['topology'] = {
            'nodes': {},
            'connections': {}
        }
    if not 'nodes' in jlab['topology']:
        jlab['topology']['nodes'] = {}
    if not 'connections' in jlab['topology']:
        jlab['topology']['connections'] = {}
    for node_id, node in  jlab['topology']['nodes'].items():
        if not 'ram' in node:
            jlab['topology']['nodes'][node_id]['ram'] = 1024
        if 'interfaces' in node:
            for interface_id, interface in node['interfaces'].items():
                # Adding default MAC address
                if node['type'] == 'qemu' and 'mac' not in node['interfaces'][interface_id]:
                    # All QEMU interfaces are ethernet
                    jlab['topology']['nodes'][node_id]['interfaces'][interface_id]['mac'] = genMac()
    return jlab

def genMac():
    # Valid MAC addressed can be:
    # x2:xx:xx:xx:xx:xx
    # x6:xx:xx:xx:xx:xx
    # xa:xx:xx:xx:xx:xx
    # xe:xx:xx:xx:xx:xx
    return '52:54:00:{:01x}{:01x}:{:01x}{:01x}:{:01x}{:01x}'.format(
        random.randint(0, 15),
        random.randint(0, 15),
        random.randint(0, 15),
        random.randint(0, 15),
        random.randint(0, 15),
        random.randint(0, 15)
    )

def getAvailableLabels(username):
    # Return available labels for a specific user
    max_labels = UserTable.query.get_or_404(username).labels
    used_labels = 0
    for active_lab in UserTable.query.get_or_404(username).active_labs:
        used_labels = used_labels + len(active_lab.nodes)
    if max_labels == -1:
        return max_labels
    return max_labels - used_labels

def printController(controller, summary = False):
    if summary:
        data =  {
            'id': controller.id,
            'inside_ip': controller.inside_ip,
            'outside_ip': controller.outside_ip,
            'master': controller.master,
            'docker_ip': controller.docker_ip
        }
    else:
        data = printController(controller, summary = True)
        data['labels'] = {}
        # Loading nodes running in this controller
        nodes = ActiveNodeTable.query.filter(ActiveNodeTable.controller_id == controller.id)
        for node in nodes:
            data['labels'][node.label] = {
                'ip': node.ip
            }
    return data

def printLab(lab, summary = False, username = None):
    if summary:
        data =  {
            'id': lab.id,
            'name': lab.name,
            'repository': lab.repository_id,
            'author': lab.author,
            'version': lab.version
        }
    else:
        data = json.loads(lab.json)
        if username != None:
            # Adding label to each node
            for node in ActiveLabTable.query.get_or_404((lab.id, username)).nodes:
                data['topology']['nodes'][str(node.node_id)]['label'] = node.label
    return data

def printRole(role):
    return {
        'role': role.role,
        'access_to': role.access_to,
        'can_write': role.can_write
    }

def printUser(user):
    data = {
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'labels': user.labels,
        'roles': []
    }
    for role in user.roles:
        data['roles'].append(role.role)
    return data

def printTask(task):
    return {
        'id': task.id,
        'status': task.status,
        'message': task.message,
        'progress': task.progress,
        'username': task.username
    }

class Auth(Resource):
    def get(self):
        user = UserTable.query.get_or_404(checkAuthz(request))
        data = {
            'status': 'success',
            'message': 'User authenticated',
            'data': printUser(user)
        }
        data['data']['active_labs'] = {}
        for active_lab in user.active_labs:
            data['data']['active_labs'][active_lab.id] = {
                'id': active_lab.id,
                'name': active_lab.name,
                'repository': active_lab.repository_id,
                'author': active_lab.author,
                'version': active_lab.version
            }
        return data

    def patch(self, role = None):
        args = patch_auth_parser.parse_args()
        username = checkAuthz(request)
        user = UserTable.query.get_or_404(username)
        for key, value in args.items():
            if key in ['name', 'password']:
                if key == 'password' and value == '':
                    # Skip empty password
                    continue
                if key == 'password':
                    setattr(user, key, hashlib.sha256(value.encode('utf-8')).hexdigest())
                    # Purging the cached user
                    cache.delete(user.username)
                else:
                    setattr(user, key, value)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'User "{}" saved'.format(user.username),
            'data': printUser(user)
        }

class BootstrapNode(Resource):
    def get(self, label = None):
        checkAuthz(request, ['admin'])
        active_node = ActiveNodeTable.query.get(label)
        node_id = active_node.node_id
        node_json = json.loads(active_node.active_lab.json)['topology']['nodes'][str(node_id)]
        if active_node.controller_id == None:
            # Controller ID not set, using local
            active_node.controller_id = config['controller']['id']
            db.session.commit()
        master = ControllerTable.query.filter(ControllerTable.master == True).one()
        controller = ControllerTable.query.get(config['controller']['id'])
        init_body = ''

        # Load header and footer
        with open('{}/templates/bootstrap_{}_header.sh'.format(app_root, node_json['type']), 'r') as fd_init_header:
            init_header = fd_init_header.read()
        with open('{}/templates/bootstrap_{}_footer.sh'.format(app_root, node_json['type']), 'r') as fd_init_footer:
            init_footer = fd_init_footer.read()

        # Configure mgm
        init_body = init_body + 'brctl addbr mgmt || exit 1\n'
        init_body = init_body + 'brctl setageing mgmt 0 || exit 1\n'
        init_body = init_body + 'ip link set dev mgmt up || exit 1\n'
        init_body = init_body + 'ip addr add 192.0.2.1/24 dev mgmt || exit 1\n'
        init_body = init_body + 'iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\n'
        init_body = init_body + 'iptables -t nat -A POSTROUTING -o mgmt -j MASQUERADE\n'
        init_body = init_body + 'iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 22 -j DNAT --to 192.0.2.254:22\n'
        init_body = init_body + 'iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 23 -j DNAT --to 192.0.2.254:23\n'
        init_body = init_body + 'iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to 192.0.2.254:80\n'
        init_body = init_body + 'iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j DNAT --to 192.0.2.254:443\n'
        init_body = init_body + 'iptables -t nat -A PREROUTING -i mgmt -p udp --dport 69 -j DNAT --to {}:69\n'.format(master.inside_ip)
        init_body = init_body + 'iptables -t nat -A PREROUTING -i mgmt -p tcp --dport 20 -j DNAT --to {}:20\n'.format(master.inside_ip)
        init_body = init_body + 'iptables -t nat -A PREROUTING -i mgmt -p tcp --dport 21 -j DNAT --to {}:21\n'.format(master.inside_ip)
        init_body = init_body + 'iptables -t nat -A PREROUTING -i mgmt -p tcp --dport 22 -j DNAT --to {}:22\n'.format(master.inside_ip)
        init_body = init_body + 'iptables -t nat -A PREROUTING -i mgmt -p tcp --dport 80 -j DNAT --to {}:80\n'.format(master.inside_ip)
        init_body = init_body + 'iptables -t nat -A PREROUTING -i mgmt -p tcp --dport 443 -j DNAT --to {}:443\n'.format(master.inside_ip)

        if node_json['type'] == 'iol':
            bin_cmd = '/data/nodes/iol.bin'
            wrapper_cmd = '/tmp/wrapper_iol.py -c {} -l {} -t -w {}'.format(controller.inside_ip, label, node_json['name'])
            if 'management' in interface and bool(interface['management']):
                # Configure management bridge
                init_body = init_body + 'tunctl -t qeth{} || exit 1\n'.format(interface_id)
                init_body = init_body + 'ip link set dev qeth{} up || exit 1\n'.format(interface_id)
                init_body = init_body + 'brctl addif mgmt qeth{} || exit 1\n'.format(interface_id)
                wrapper_cmd = wrapper_cmd + ' -m qeth{}'.format(interface_id)
                bin_cmd = bin_cmd + ' -netdev tap,id=eth{},ifname=qeth{},script=no,downscript=no -device virtio-net,netdev=eth{},mac=52:54:00:00:00:00'.format(interface_id, interface_id, interface_id)
        elif node_json['type'] == 'qemu':
            bin_cmd = '/usr/bin/qemu-system-x86_64'
            wrapper_cmd = '/tmp/wrapper_qemu.py -c {} -l {}'.format(controller.inside_ip, label)
            if node_json['subtype'] == 'vyos':
                bin_cmd = bin_cmd + ' -boot order=c -drive file=/data/node/hda.qcow2,if=virtio,format=qcow2 -enable-kvm -m {}M -serial telnet:0.0.0.0:5023,server,nowait -monitor telnet:0.0.0.0:5024,server,nowait -nographic'.format(node_json['ram'])
                for interface_id, interface in sorted(node_json['interfaces'].items()):
                    interface_id = int(interface_id)
                    if 'management' in interface and bool(interface['management']):
                        # Configure management bridge
                        init_body = init_body + 'tunctl -t qeth{} || exit 1\n'.format(interface_id)
                        init_body = init_body + 'ip link set dev qeth{} up || exit 1\n'.format(interface_id)
                        init_body = init_body + 'brctl addif mgmt qeth{} || exit 1\n'.format(interface_id)
                        wrapper_cmd = wrapper_cmd + ' -m qeth{}'.format(interface_id)
                        bin_cmd = bin_cmd + ' -netdev tap,id=eth{},ifname=qeth{},script=no,downscript=no -device virtio-net,netdev=eth{},mac=52:54:00:00:00:00'.format(interface_id, interface_id, interface_id)
                    else:
                        init_body = init_body + 'tunctl -t veth{} || exit 1\n'.format(interface_id)
                        init_body = init_body + 'ip link set dev veth{} up || exit 1\n'.format(interface_id)
                        init_body = init_body + 'tunctl -t qeth{} || exit 1\n'.format(interface_id)
                        init_body = init_body + 'ip link set dev qeth{} up || exit 1\n'.format(interface_id)
                        init_body = init_body + 'brctl addbr br{} || exit 1\n'.format(interface_id)
                        init_body = init_body + 'brctl setageing br{} 0 || exit 1\n'.format(interface_id)
                        init_body = init_body + 'ip link set dev br{} up || exit 1\n'.format(interface_id)
                        init_body = init_body + 'brctl addif br{} veth{} || exit 1\n'.format(interface_id, interface_id)
                        init_body = init_body + 'brctl addif br{} qeth{} || exit 1\n'.format(interface_id, interface_id)
                        bin_cmd = bin_cmd + ' -netdev tap,id=eth{},ifname=qeth{},script=no,downscript=no -device virtio-net,netdev=eth{},mac={}'.format(interface_id, interface_id, interface_id, interface['mac'])
            init_body = init_body + wrapper_cmd + ' -- ' + bin_cmd + ' & \n'
            init_body = init_body + 'QEMU_PID=$!\n'
            init_body = init_body + 'wait ${QEMU_PID}\n'

        init_script = init_header + init_body + init_footer
        return send_file(io.BytesIO(init_script.encode()), attachment_filename = 'init', mimetype = 'text/x-shellscript')


class Controller(Resource):
    def get(self, controller_id = None):
        checkAuthz(request, ['admin'])
        if not controller_id:
            # List all controllers
            summary = True
            controllers = ControllerTable.query.order_by(ControllerTable.id)
        else:
            # List a single controller if exists, else 404
            summary = False
            controllers = [ControllerTable.query.get_or_404(controller_id)]
        data = {}
        for controller in controllers:
            # Print each controller
            data[controller.id] = printController(controller, summary = summary)
        return {
            'status': 'success',
            'message': 'Controller(s) found',
            'data': data
        }

class Lab(Resource):
    def delete(self, lab_id = None):
        username = checkAuthz(request)
        args = delete_lab_parser.parse_args()
        if not lab_id:
            # No lab has been selected
            abort(400)
        else:
            active_lab = ActiveLabTable.query.get((lab_id, username))
            lab = LabTable.query.get(lab_id)
        if not active_lab and not lab:
            abort(404)
        if active_lab:
            # If an active lab exists for the user, it can be deleted by the user himself
            db.session.delete(active_lab)
        if lab and args['commit'] == True:
            # If a lab exists, it can be deleted by an authorized user only
            checkAuthzPath(request, [lab.repository_id, lab.name], True)
            db.session.delete(lab)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Lab "{}" deleted'.format(lab_id)
        }

    def get(self, lab_id = None):
        username = checkAuthz(request)
        if not lab_id:
            # List all labs
            summary = True
            labs = LabTable.query.order_by(LabTable.name)
        else:
            # List a single lab if exists, else 404
            summary = False
            active_lab = ActiveLabTable.query.get((lab_id, username))
            lab = LabTable.query.get(lab_id)
            if active_lab:
                # Found an active lab
                labs = [active_lab]
            elif lab:
                # Found a lab
                labs = [lab]
                jlab = json.loads(lab.json)
                # Make the lab active
                activateLab(username, jlab)
            else:
                abort(404)
        data = {}
        for lab in labs:
            # Print each lab
            data[lab.id] = printLab(lab, summary = summary, username = username)
        return {
            'status': 'success',
            'message': 'Lab(s) found',
            'data': data
        }

    def post(self):
        args = add_lab_parser.parse_args()
        username = checkAuthzPath(request, [args['repository']], True)
        jlab = {
            'id': str(uuid.uuid4()),
            'name': args['name'],
            'repository': args['repository'],
            'author': args['author'],
            'version': args['version'],
            'topology': args['topology']
        }
        jlab = fixjLab(jlab)
        # Make the lab active
        activateLab(username, jlab)
        if args['commit']:
            # Write to file, add to git and commit
            lab_file = '{}/{}/{}.{}'.format(config['app']['lab_repository'], jlab['repository'], jlab['id'], config['app']['lab_extension'])
            lab = LabTable(
                id = jlab['id'],
                name = jlab['name'],
                repository_id = jlab['repository'],
                author = jlab['author'],
                version = jlab['version'],
                json = json.dumps(jlab, separators = (',', ':'), sort_keys = True),
            )
            with open(lab_file, 'w') as lab_fd:
                json.dump(printLab(lab), lab_fd, sort_keys = True, indent = 4)
            sh.git('-C', '{}/{}'.format(config['app']['lab_repository'], lab.repository_id), 'add', lab_file, _bg = False)
            sh.git('-C', '{}/{}'.format(config['app']['lab_repository'], lab.repository_id), 'commit', '-m', 'Added lab {} ("{}")'.format(lab.id, lab.name))
            db.session.add(lab)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Lab "{}" added'.format(lab.id),
            'data': printLab(lab, username = username)
        }

class Repository(Resource):
    # TODO: only admin edit remote
    # TODO: all users with write permission push
    # TODO: all users with write permission commit -> solo se un lab viene salvato (i lab vengono caricati e messi su in db. editati da db. solo save li porta sul repo con commit)
    # TODO: all users with write permission pull
    # TODO: allo startup pull + scan dei repo con aggiunta al db dei lab
    def delete(self, repository = None):
        username = checkAuthz(request, ['admin'])
        if not repository:
            # No repository has been selected
            abort(400)
        elif repository == 'local':
            # Repository 'local' cannot be deleted
            abort(403)
        elif not os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository)):
            # Repository does not exist
            abort(404)
        t = deleteGit.apply_async((username, repository,))
        return {
            'status': 'enqueued',
            'message': 'Task "{}" enqueued to the batch manager'.format(t),
            'task': str(t)
        }

    def post(self):
        args = add_repository_parser.parse_args()
        checkAuthz(request, ['admin'])
        if args['repository'] == 'local':
            # local is a reserved repository
            abort(400)
        t = addGit.apply_async((username, args['repository'], args['url'], args['username'], args['password']))
        return {
            'status': 'enqueued',
            'message': 'Task "{}" enqueued to the batch manager'.format(t),
            'task': str(t)
        }

class Role(Resource):
    def delete(self, role = None):
        checkAuthz(request, ['admin'])
        if not role:
            # No role has been selected
            abort(400)
        elif role == 'admin':
            # Role 'admin' cannot be deleted
            abort(403)
        else:
            # Get the role if exists, else 404
            role = RoleTable.query.get_or_404(role)
        db.session.delete(role)
        db.session.commit()
        for user in role.users:
            # Purging the cached user
            cache.delete(user.username)
        return {
            'status': 'success',
            'message': 'Role "{}" deleted'.format(role.role)
        }

    def get(self, role = None):
        checkAuthz(request, ['admin'])
        if not role:
            # List all roles
            roles = RoleTable.query.order_by(RoleTable.role)
        else:
            # List a single role if exists, else 404
            roles = [RoleTable.query.get_or_404(role)]
        data = {}
        for role in roles:
            # Print each role
            data[role.role] = printRole(role)
        return {
            'status': 'success',
            'message': 'Role(s) found',
            'data': data
        }

    def patch(self, role = None):
        args = patch_role_parser.parse_args()
        checkAuthz(request, ['admin'])
        if not role:
            # No role has been selected
            abort(400)
        else:
            # Get the role if exists, else 404
            role = RoleTable.query.get_or_404(role)
        for key, value in args.items():
            if key in ['access_to', 'can_write']:
                setattr(role, key, value)
        db.session.commit()
        for user in role.users:
            # Purging the cached user
            cache.delete(user.username)
        return {
            'status': 'success',
            'message': 'Role "{}" saved'.format(role.role),
            'data': printRole(role)
        }

    def post(self):
        args = add_role_parser.parse_args()
        checkAuthz(request, ['admin'])
        if RoleTable.query.get(args['role']):
            # Role eady exists
            abort(409)
        role = RoleTable(
            role = args['role'],
            can_write = args['can_write'],
            access_to = args['access_to']
        )
        db.session.add(role)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Role "{}" added'.format(role.role),
            'data': printRole(role)
        }

class Routing(Resource):
    def get(self, role = None):
        checkAuthz(request, ['admin'])
        nodes = ActiveNodeTable.query.order_by(ActiveNodeTable.label)
        controllers = []
        for controller in ControllerTable.query:
            controllers.append(controller.id)
        node_controllers = {}
        for node in nodes:
            node_controller = 0 if node.controller_id not in controllers else node.controller_id
            node_controllers[node.label] = node_controller

        data = {}
        for node in nodes:
            src_label = node.label
            for interface in node.interfaces:
                if not node.label in data:
                    data[node.label] = {}
                data[node.label][interface.id] = {
                    'dst_controller': node_controllers[interface.dst_label],
                    'dst_label': interface.dst_label,
                    'dst_if' : interface.dst_if
                }
        return {
            'status': 'success',
            'message': 'Routing table found',
            'data': data
        }

class Task(Resource):
    def get(self, task_id = None):
        username = checkAuthz(request)
        if not task_id:
            # List all tasks
            # TODO from this user only, or all for admins
            tasks = TaskTable.query.order_by(TaskTable.id)
        else:
            # List a single task if exists, else 404
            # TODO task can be pending: see https://blog.miguelgrinberg.com/post/using-celery-with-flask (task = long_task.AsyncResult(task_id))
            tasks = [TaskTable.query.get_or_404(task_id)]
        data = {}
        for task in tasks:
            # Print each task
            data[task.id] = printTask(task)
        return {
            'status': 'success',
            'message': 'Task(s) found',
            'data': data
        }

class User(Resource):
    def delete(self, username = None):
        checkAuthz(request, ['admin'])
        if not username:
            # No user has been selected
            abort(400)
        elif username == 'admin':
            # User 'admin' cannot be deleted
            abort(403)
        else:
            # Get the user if exists, else 404
            user = UserTable.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        # Purging the cached user
        cache.delete(user.username)
        return {
            'status': 'success',
            'message': 'User "{}" deleted'.format(user.username)
        }

    def get(self, username = None):
        checkAuthz(request, ['admin'])
        if not username:
            # List all users
            users = UserTable.query.order_by(UserTable.username)
        else:
            # List a single user if exists, else 404
            users = [UserTable.query.get_or_404(username)]
        data = {}
        for user in users:
            # Print each user
            data[user.username] = printUser(user)
        return {
            'status': 'success',
            'message': 'User(s) found',
            'data': data
        }

    def patch(self, username = None):
        args = patch_user_parser.parse_args()
        checkAuthz(request, ['admin'])
        if not username:
            # No user has been selected
            abort(400)
        else:
            # Get the user if exists, else 404
            user = UserTable.query.get_or_404(username)
        for key, value in args.items():
            if key in ['email', 'labels', 'name']:
                setattr(user, key, value)
            if key == 'password':
                setattr(user, key, hashlib.sha256(value.encode('utf-8')).hexdigest())
            if key == 'roles':
                # Removing previous roles and add new ones
                user.roles = []
                for role in value:
                    user.roles.append(RoleTable.query.get_or_404(role))
        db.session.commit()
        # Purging the cached user
        cache.delete(user.username)
        return {
            'status': 'success',
            'message': 'User "{}" saved'.format(user.username),
            'data': printUser(user)
        }

    def post(self):
        args = add_user_parser.parse_args()
        checkAuthz(request, ['admin'])
        if UserTable.query.get(args['username']):
            # User already exists
            abort(409)
        user = UserTable(
            username = args['username'],
            password = hashlib.sha256(args['password'].encode('utf-8')).hexdigest(),
            name = args['name'],
            email = args['email'],
            labels = args['labels']
        )
        user.roles = []
        for role in args['roles']:
            # Adding all roles
            user.roles.append(RoleTable.query.get_or_404(role))
        db.session.add(user)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'User "{}" added'.format(user.username),
            'data': printUser(user)
        }
