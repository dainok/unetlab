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

def printRepository(repository):
    data =  {
        'id': repository.id,
        'url': repository.url,
        'username': repository.username
    }
    return data

def printRole(role):
    return {
        'role': role.role,
        'access_to': role.access_to,
        'can_write': role.can_write
    }

def printRouter(router, summary = False):
    if summary:
        data =  {
            'id': router.id,
            'inside_ip': router.inside_ip,
            'outside_ip': router.outside_ip,
        }
    else:
        data = printRouter(router, summary = True)
        data['labels'] = {}
        # Loading nodes running in this controller
        nodes = ActiveNodeTable.query.filter(ActiveNodeTable.router_id == router.id)
        for node in nodes:
            data['labels'][node.label] = {
                'ip': node.ip
            }
    return data

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
        username = checkAuthz(request)
        args = auth_parser_patch(username)
        user = UserTable.query.get_or_404(username)
        setattr(user, 'password', hashlib.sha256(args['password'].encode('utf-8')).hexdigest())
        cache.delete(user.username)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'User "{}" saved'.format(user.username),
            'data': printUser(user)
        }

class BootstrapRouter(Resource):
    def get(self, router_id = None):
        checkAuthz(request, ['admin'])
        router = RouterTable.query.get_or_404(router_id)
        init_body = ''

        # Load header and footer
        with open('{}/templates/bootstrap_router_header.sh'.format(app_root), 'r') as fd_init_header:
            init_header = fd_init_header.read()
        with open('{}/templates/bootstrap_router_footer.sh'.format(app_root), 'r') as fd_init_footer:
            init_footer = fd_init_footer.read()

        init_script = init_header + init_body + init_footer
        return send_file(io.BytesIO(init_script.encode()), attachment_filename = 'init', mimetype = 'text/x-shellscript')

class BootstrapNode(Resource):
    def get(self, label = None):
        checkAuthz(request, ['admin'])
        active_node = ActiveNodeTable.query.get_or_404(label)
        node_id = active_node.node_id
        node_json = json.loads(active_node.active_lab.json)['topology']['nodes'][str(node_id)]
        if active_node.router_id == None:
            # Router ID not set, using local
            # TODO: not needed, because start will set it
            active_node.router_id = 0
            db.session.commit()
        router = RouterTable.query.get_or_404(active_node.router_id)
        init_body = ''

        # Load header and footer
        with open('{}/templates/bootstrap_{}_header.sh'.format(app_root, node_json['type']), 'r') as fd_init_header:
            init_header = fd_init_header.read()
        with open('{}/templates/bootstrap_{}_footer.sh'.format(app_root, node_json['type']), 'r') as fd_init_footer:
            init_footer = fd_init_footer.read()

        # Configure mgmt
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
            wrapper_cmd = '/tmp/wrapper_iol.py -c {} -l {} -t -w {}'.format(controller.inside_ip, label, node_json['name'])
            bin_cmd = '/data/node/iol.bin -n 4096 -q'
            if 'iol_id' in node_json:
                iol_id = node_json['iol_id']
            else:
                iol_id = random.randint(1, 1024)
            if 'memory' in node_json:
                bin_cmd * bin_cmd + ' -m {}'.format(node_json['memory'])
            if 'ethernet' in node_json:
                bin_cmd = bin_cmd + ' -e {}'.format(-(-node_json['ethernet'] // 4))
            if 'serial' in node_json:
                bin_cmd = bin_cmd + ' -s {}'.format(-(-node_json['serial'] // 4))
            bin_cmd = bin_cmd + ' {}'.format(iol_id)
            init_body = init_body + 'if [ ! -f /data/node/nvram_{:05} ]; then\n'.format(iol_id)
            init_body = init_body + '\tfind /data/node -name "nvram_*" -exec mv {{}} /data/node/nvram_{:05} \;\n'.format(iol_id)
            init_body = init_body + 'fi\n'
            # Configure management bridge
            init_body = init_body + 'tunctl -t veth0 || exit 1\n'
            init_body = init_body + 'ip link set dev veth0 up || exit 1\n'
            init_body = init_body + 'brctl addif mgmt veth0 || exit 1\n'
            init_body = init_body + 'cd /data/node || exit 1\n'
            for interface_id, interface in sorted(node_json['interfaces'].items()):
                if 'management' in interface and bool(interface['management']):
                    wrapper_cmd = wrapper_cmd + ' -m {}'.format(interface_id)
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
        init_body = init_body + 'BIN_PID=$!\n'
        init_body = init_body + 'wait ${BIN_PID}\n'
        init_script = init_header + init_body + init_footer
        return send_file(io.BytesIO(init_script.encode()), attachment_filename = 'init', mimetype = 'text/x-shellscript')

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
        else:
            lab = ActiveLabTable.query.get((jlab['id'], username))
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Lab "{}" added'.format(lab.id),
            'data': printLab(lab, username = username)
        }

class Node(Resource):
    def get(self, label = None, action = None):
        active_node = ActiveNodeTable.query.get_or_404(label)
        router_id = active_node.router_id
        if router_id == None:
            active_node.router_id = 0
            db.commit()
        node_ip = active_node.ip
        username = checkAuthzPath(request, [active_node.active_lab.repository_id, active_node.active_lab.name])
        jlab = json.loads(active_node.active_lab.json)
        node_name = jlab['topology']['nodes'][str(active_node.node_id)]['name']
        if action == 'start':
            node_image = jlab['topology']['nodes'][str(active_node.node_id)]['image']
            node_type = jlab['topology']['nodes'][str(active_node.node_id)]['type']
            t = startNode.apply_async((username, label, node_name, active_node.node_id, node_type, node_image, node_ip, router_id))
        elif action == 'stop':
            t = stopNode.apply_async((label, name, active_node.node_id, router_id))
        elif action == 'restart':
            t = restartNode.apply_async((label, name, active_node.node_id, router_id))
        elif action == 'delete':
            t = deleteNode.apply_async((label, name, active_node.node_id, router_id))
        else:
            abort(404)
        return {
            'status': 'enqueued',
            'message': 'Task "{}" enqueued to the batch manager'.format(t),
            'task': str(t)
        }

class Repository(Resource):
    def delete(self, repository_id = None):
        username = checkAuthz(request, ['admin'])
        if not repository_id:
            # No repository has been selected
            abort(400)
        elif repository_id == 'local':
            # Repository 'local' cannot be deleted
            abort(403)
        elif not os.path.isdir('{}/{}'.format(config['app']['lab_repository'], repository_id)):
            # Repository does not exist
            abort(404)
        t = deleteGit.apply_async((username, repository_id,))
        return {
            'status': 'enqueued',
            'message': 'Task "{}" enqueued to the batch manager'.format(t),
            'task': str(t)
        }

    def get(self, repository_id = None):
        username = checkAuthz(request, ['admin'])
        if not repository_id:
            # List all repositories
            repositories = RepositoryTable.query.order_by(RepositoryTable.query.order_by.id)
        else:
            # List a single repository if exists, else 404
            repositories = [RepositoryTable.query.get_or_404(repository_id)]
        data = {}
        for repository in repositories:
            # Print each repository
            data[repository.id] = printRepository(repository)
        return {
            'status': 'success',
            'message': 'Repository(ies) found',
            'data': data
        }

    def patch(self, repository_id = None):
        args = patch_repository_parser.parse_args()
        checkAuthz(request, ['admin'])
        if not repository_id:
            # No repository has been selected
            abort(400)
        else:
            # Get the repository if exists, else 404
            repository = RepositoryTable.query.get_or_404(repository_id)
        for key, value in args.items():
            if key in ['url', 'username', 'password']:
                setattr(repository, key, value)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Repository "{}" saved'.format(repository.id),
            'data': printRepository(repository)
        }

    def post(self):
        args = add_repository_parser.parse_args()
        username = checkAuthz(request, ['admin'])
        if args['repository'] == 'local':
            # local is a reserved repository
            abort(400)
        if not args['username']:
            args['username'] = None
            args['password'] = None
        t = addGit.apply_async((username, args['repository'], args['url'], args['username'], args['password']))
        return {
            'status': 'enqueued',
            'message': 'Task "{}" enqueued to the batch manager'.format(t),
            'task': str(t)
        }

class Role(Resource):
    def delete(self, role = None):
        checkAuthz(request, ['admin'])
        # Get the role if exists, else 404
        role_parser_get(role)
        role = RoleTable.query.get(role)
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
            role_parser_get(role)
            roles = [RoleTable.query.get(role)]
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
        checkAuthz(request, ['admin'])
        args = role_parser_patch(role)
        role = RoleTable.query.get(role)
        for key, value in args.items():
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
        checkAuthz(request, ['admin'])
        args = role_parser_post()
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

class Router(Resource):
    def delete(self, router_id = None):
        checkAuthz(request, ['admin'])
        if not router_id:
            # No router has been selected
            abort(400)
        else:
            # Get the router if exists, else 404
            router = RouterTable.query.get_or_404(router_id)
        db.session.delete(router)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Router "{}" deleted'.format(router.id)
        }

    def get(self, router_id = None):
        checkAuthz(request, ['admin'])
        if router_id == None:
            # List all routers
            summary = True
            routers = RouterTable.query.order_by(RouterTable.id)
        else:
            # List a single controller if exists, else 404
            summary = False
            routers = [RouterTable.query.get_or_404(router_id)]
        data = {}
        for router in routers:
            # Print each router
            data[router.id] = printRouter(router, summary = summary)
        return {
            'status': 'success',
            'message': 'Router(s) found',
            'data': data
        }

    def patch(self, router_id = None):
        args = patch_router_parser.parse_args()
        checkAuthz(request, ['admin'])
        if not router_id:
            # No router has been selected
            abort(400)
        else:
            # Get the router if exists, else 404
            router = RouterTable.query.get_or_404(router_id)
        for key, value in args.items():
            if key in ['inside_ip', 'outside_ip']:
                setattr(router, key, value)
        db.session.commit()
        return {
            'status': 'success',
            'message': 'Router "{}" saved'.format(router.id),
            'data': printRouter(router)
        }

    def post(self):
        args = add_router_parser.parse_args()
        checkAuthz(request, ['admin'])
        router = RouterTable.query.get(args['id'])
        if router:
            # Router already exists (registering)
            router.inside_ip = args['inside_ip']
            message = 'Router "{}" registered'.format(router.id)
        else:
            # New router
            router = RouterTable(
                id = args['id'],
                inside_ip = args['inside_ip'],
                outside_ip = args['outside_ip']
            )
            message = 'Router "{}" added'.format(router.id)
            db.session.add(router)
        db.session.commit()
        return {
            'status': 'success',
            'message': message,
            'data': printRouter(router)
        }

class Routing(Resource):
    def get(self, role = None):
        checkAuthz(request, ['admin'])
        nodes = ActiveNodeTable.query.order_by(ActiveNodeTable.label)
        routers = []
        for router in RouterTable.query:
            routers.append(router.id)
        node_routers = {}
        for node in nodes:
            node_router = 0 if node.router_id not in routers else node.router_id
            node_routers[node.label] = node_router

        data = {}
        for node in nodes:
            src_label = node.label
            for interface in node.interfaces:
                if not node.label in data:
                    data[node.label] = {}
                data[node.label][interface.id] = {
                    'dst_router': node_routers[interface.dst_label],
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
        # Todo should list also running tasks from celery
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
        # Get the user if exists, else 404
        user_parser_get(username)
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
            user_parser_get(username)
            users = [UserTable.query.get(username)]
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
        checkAuthz(request, ['admin'])
        args = user_parser_patch(username)
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
        checkAuthz(request, ['admin'])
        args = user_parser_post()
        user = UserTable(
            username = args['username'],
            password = hashlib.sha256(args['password'].encode('utf-8')).hexdigest(),
            name = args['name'],
            email = args['email'],
            labels = args['labels']
        )
        user.roles = []
        if not args['roles']:
            args['roles'] = []
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

