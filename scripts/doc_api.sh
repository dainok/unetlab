#!/bin/bash

COOKIE=/tmp/cookie
USERNAME=admin
PASSWORD=unl

cat << EOF > /usr/src/unetlab.github.io/_posts/2015-09-01-using-unetlab-apis.md
---
layout: post
published: true
title: "Using UNetLab APIs"
excerpt:
  "HowTo use UNetLab API."
section: "HowTo"
authors:
- andrea
tags:
- UNetLab
- HowTo
---
UNetLab APIs use JSend, a JSON response in the following syntax:

~~~
{
	"code": 404,
	"message": "Requested folder does not exist (60008).",
	"status": "fail"
}
~~~

Code is the HTTP response code, message is a simple string explaining what is going on, and status is a single word explaining the response.
Five status type are used:

* success for 20x HTTP codes;
* unauthorized for 400 HTTP code, meaning that the user session has timed out;
* unauthorized for 401 HTTP code, meaning that user should login;
* forbidden for 403 HTTP code, meaning that user does not have enough privileges;
* fail for other 40x HTTP codes;
* error for 50x HTTP codes.

The default Web-UI uses only APIs, so this is an essential part to develop new Web-UI themes, integration and so on.
Mind that each user can login from a single location only. If the same user login twice, the second login disable the first one.

## Authentication

The following API requests are involved on login and logout process. All other API requests require an authenticated user.

### Login

\`curl -s -b $COOKIE -c $COOKIE -X POST -d '{"username":"${USERNAME}","password":"${PASSWORD}"}' http://127.0.0.1/api/auth/login\`

A successful login provides the following output:

~~~
`curl -s -b $COOKIE -c $COOKIE -X POST -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}" http://127.0.0.1/api/auth/login | python -m json.tool`
~~~

### User Info

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/auth\`

An authenticated user can get its own information:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/auth | python -m json.tool`
~~~

### Logout

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/auth/logout\`

All users can logout, this request cannot fail:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/auth/logout | python -m json.tool`
~~~
`curl -s -b $COOKIE -c $COOKIE -X POST -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}" http://127.0.0.1/api/auth/login > /dev/null`
## System status

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/status\`

An authenticated user can get system statistics:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/status | python -m json.tool`
~~~

## List node templates

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/list/templates/\`

An authenticated user can list all available node templates:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/list/templates/ | python -m json.tool`
~~~

A single template can be listed:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/list/templates/iol\`

All available images for the selected template will be included in the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/list/templates/iol | python -m json.tool`
~~~

## List network types

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/list/networks\`

An authenticated user can list all available network types:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/list/networks | python -m json.tool`
~~~

## List user roles

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/list/roles\`

An authenticated user can list all user roles:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/list/roles | python -m json.tool`
~~~

## Navigating between folders

The following API requests allow to manages folders and labs as files.

### List content inside a folder

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/folders/Andrea\`

An authenticated user can list what is inside a folder:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/folders/Andrea | python -m json.tool`
~~~

Folders and labs are listed using different arrays.

### Add a new folder

\`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"path":"/Andrea/Folder 3","name":"New Folder"}' -H 'Content-type: application/json' http://127.0.0.1/api/folders\`

An authenticated user can add a folder inside a specific path:

~~~
`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"path":"/Andrea/Folder 3","name":"New Folder"}' -H 'Content-type: application/json' http://127.0.0.1/api/folders | python -m json.tool`
~~~

### Move/rename an existent folder

\`curl -s -c $COOKIE -b $COOKIE -X PUT -d '{"path":"/Andrea/Folder 3/Test Folder"}' -H 'Content-type: application/json' http://127.0.0.1/api/folders/Andrea/Folder%203/New%20Folder\`

An authenticated user can add a folder inside a specific path:

~~~
`curl -s -c $COOKIE -b $COOKIE -X PUT -d '{"path":"/Andrea/Folder 3/Test Folder"}' -H 'Content-type: application/json' http://127.0.0.1/api/folders/Andrea/Folder%203/New%20Folder | python -m json.tool`
~~~

### Delete an existing folder

\`curl -s -c $COOKIE -b $COOKIE -X DELETE -H 'Content-type: application/json' http://127.0.0.1/api/folders/Andrea/Folder%203/Test%20Folder\`

An authenticated user can delete an existing folder:

~~~
`curl -s -c $COOKIE -b $COOKIE -X DELETE -H 'Content-type: application/json' http://127.0.0.1/api/folders/Andrea/Folder%203/Test%20Folder | python -m json.tool`
~~~

## Managing users

The following API requests allow to manage UNetLab users and permissions.

### Get a user

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/users/\`

An authenticated user can get all UNetLab users:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/users/ | python -m json.tool`
~~~

A single user can be retrieved:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/users/admin\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/users/admin | python -m json.tool`
~~~

### Add a new user

\`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"username":"testuser","name":"Test User","email":"test@unetlab.com","password":"testpassword1","role":"user","expiration":"-1","pod":127,"pexpiration":"1451520000"}' -H 'Content-type: application/json' http://127.0.0.1/api/users\`

An authenticated user can add a new UNetLab user:

~~~
`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"username":"testuser","name":"Test User","email":"test@unetlab.com","password":"testpassword1","role":"user","expiration":"-1","pod":127,"pexpiration":"1451520000"}' -H 'Content-type: application/json' http://127.0.0.1/api/users | python -m json.tool`
~~~

Parameters:

* email: the email address of the user;
* expiration: date until the user is valid (UNIX timestamp) or \`-1\` if never expires;
* name: a description for the user, usually salutation;
* password (mandatory): the user password used to login;
* role: see "List user roles";
* username (mandatory): a unique alphanumeric string used to login;

### Edit an user

\`curl -s -c $COOKIE -b $COOKIE -X PUT -d '{"name":"New Test User","email":"testuser@unetlab.com","password":"newpassword","role":"user","expiration":"1451520000","pod":127,"pexpiration":"-1"}' -H 'Content-type: application/json' http://127.0.0.1/api/users/testuser\`

An authenticated user can edit an existent UNetLab user:

~~~
`curl -s -c $COOKIE -b $COOKIE -X PUT -d '{"name":"New Test User","email":"testuser@unetlab.com","password":"newpassword","role":"user","expiration":"1451520000","pod":127,"pexpiration":"-1"}' -H 'Content-type: application/json' http://127.0.0.1/api/users/testuser | python -m json.tool`
~~~

Parameters:

* email: the email address of the user;
* expiration: date until the user is valid (UNIX timestamp) or \`-1\` if never expires;
* name: a description for the user, usually salutation;
* password: the user password used to login;
* role: see "List user roles";

### Delete an user

\`curl -s -c $COOKIE -b $COOKIE -X DELETE -H 'Content-type: application/json' http://127.0.0.1/api/users/testuser\`

An authenticated user can delete an existent UNetLab user:

~~~
`curl -s -c $COOKIE -b $COOKIE -X DELETE -H 'Content-type: application/json' http://127.0.0.1/api/users/testuser | python -m json.tool`
~~~

## Managing labs

The following API requests allow to manage labs and object inside a lab, like nodes, networks... and so on.

### Get a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl\`

An authenticated user can retrieve a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl | python -m json.tool`
~~~

### Get one or all networks configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/networks\`

An authenticated user can retrieve all configured networks in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/networks | python -m json.tool`
~~~

A single network can be retrieved:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/networks/1\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/networks/1 | python -m json.tool`
~~~

### Get all remote endpoint for both ethernet and serial interfaces

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/links\`

An authenticated user can retrieve all available endpoint in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/links | python -m json.tool`
~~~

This API is useful when a user need to connect a node.

### Get one or all nodes configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes\`

An authenticated user can retrieve all configured nodes in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes | python -m json.tool`
~~~

A single node can be retrieved:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1 | python -m json.tool`
~~~

### Start one or all nodes configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/start\`

An authenticated user can start all configured nodes in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/start | python -m json.tool`
~~~

A single node can be started:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/start\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/start | python -m json.tool`
~~~

### Stop one or all nodes configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/stop\`

An authenticated user can stop all configured nodes in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/stop | python -m json.tool`
~~~

A single node can be stopped:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/stop\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/stop | python -m json.tool`
~~~

### Wipe one or all nodes configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/wipe\`

An authenticated user can wipe all configured nodes in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/wipe | python -m json.tool`
~~~

Wiping means delete all user config, included startup-config, VLANs, and so on. Next start will rebuild node from selected image.
A single node can be wiped:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/wipe\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/wipe | python -m json.tool`
~~~

### Export one or all nodes configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/export\`

An authenticated user can export all configured nodes in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/export | python -m json.tool`
~~~

Exporting means save startup-config into the lab file. Starting a node after a wipe will load the previously exported startup-config.
A single node can be wiped:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/export\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/export | python -m json.tool`
~~~

### Get configured intefaces from a node

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/interfaces\`

An authenticated user can retrieve all configured interfaces from a node:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/nodes/1/interfaces | python -m json.tool`
~~~

### Get the lab topology

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/topology\`

An authenticated user can get lab topology:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/topology | python -m json.tool`
~~~

### Get one or all pictures configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/pictures\`

An authenticated user can get all configured pictures in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/pictures | python -m json.tool`
~~~

A single picture can be retrieved:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/pictures/1\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/pictures/1 | python -m json.tool`
~~~

The data picture can be retrieved using a different request:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Lab%201.unl/pictures/1/data/32/32\`

The resized picture is generated with original aspect-ratio using given values as maximum witdh/lenght.

### Create a new lab

\`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"path":"/Andrea/Folder 3","name":"New Lab","version":"1","author":"Andrea Dainese","description":"A new demo lab","body":"Lab usage and guide"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs\`

An authenticated user can create a new lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"path":"/Andrea/Folder 3","name":"New Lab","version":"1","author":"Andrea Dainese","description":"A new demo lab","body":"Lab usage and guide"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs | python -m json.tool`
~~~

### Move an existing lab to a different folder

\`curl -s -c $COOKIE -b $COOKIE -X PUT -d '{"path":"/Andrea/Folder 2"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%203/New%20Lab.unl\`

~~~
`curl -s -c $COOKIE -b $COOKIE -X PUT -d '{"path":"/Andrea/Folder 2"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%203/New%20Lab.unl/move | python -m json.tool`
~~~

### Edit an existing lab

\`curl -s -c $COOKIE -b $COOKIE -X PUT -d '{"name":"Different Lab","version":"2","author":"AD","description":"A different demo lab"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%202/New%20Lab.unl\`

An authenticated user can edit an existing lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X PUT -d '{"name":"Different Lab","version":"2","author":"AD","description":"A different demo lab"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%202/New%20Lab.unl | python -m json.tool`
~~~

The request can set only one single parameter. Optional paramiter can be reverted to the default setting an empty string "".

### Add a new network to a lab

\`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"type":"bridge","name":"Core Network","left":"35%","top":"25%"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%202/Different%20Lab.unl/networks\`

An authenticated user can add a network to an existing lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"type":"bridge","name":"Core Network","left":"35%","top":"25%"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%202/Different%20Lab.unl/networks | python -m json.tool`
~~~

Parameters:

* left: mergin from left, in percentage (i.e. \`35%\`), default is a random value between \`30%\` and \`70%\`;
* name: network name (i.e. \`Core Network\`), default is \`NetX\` (\`X = network_id\`);
* top: margin from top, in percentage (i.e. \`25%\`), default is a random value between \`30%\` and \`70%\`;
* type (mandatory): see "List network types".

### Add a new node to a lab

\`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"type":"qemu","template":"vios","config":"Unconfigured","delay":0,"icon":"Router.png","image":"vios-adventerprisek9-m-15.5.3M","name":"Core Router 1","left":"35%","top":"25%","ram":"1024","console":"telnet","cpu":1,"ethernet":2,"uuid":"641a4800-1b19-427c-ae87-4a8ee90b7790"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%202/Different%20Lab.unl/nodes\`

An authenticated user can add a node to an existing lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"type":"qemu","template":"vios","config":"Unconfigured","delay":0,"icon":"Router.png","image":"vios-adventerprisek9-m-15.5.3M","name":"Core Router 1","left":"35%","top":"25%","ram":"1024","console":"telnet","cpu":1,"ethernet":2,"uuid":"641a4800-1b19-427c-ae87-4a8ee90b7790"}' -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%202/Different%20Lab.unl/nodes | python -m json.tool`
~~~

Parameters:

* config: can be \`Unconfigured\` or \`Saved\`, default is \`Unconfigured\`;
* delay: seconds to wait before starting the node, default is \`0\`;
* icon: icon (located under \`/opt/unetlab/html/images/icons/\`) used to display the node, default is \`Router.png\`;
* image: image used to start the node, default is latest included in "List node templates";
* left: mergin from left, in percentage (i.e. \`35%\`), default is a random value between \`30%\` and \`70%\`;
* name: node name (i.e. "\`Core1\`"), default is \`NodeX\` (\`X = node_id\`);
* ram: MB of RAM configured for the node, default is \`1024\`;
* template (mandatory): see "List node templates";
* top: margin from top, in percentage (i.e. \`25%\`), default is a random value between \`30%\` and \`70%\`;
* type (mandatory): can be \`iol\`, \`dynamips\` or \`qemu\`.

Parameters for IOL nodes:

* ethernet: number of ethernet porgroups (each portgroup configures four interfaces), default is \`2\`;
* nvram: size of NVRAM in KB, default is \`1024\`;
* serial: number of serial porgroups (each portgroup configures four interfaces), default is \`2\`.

Parameters for Dynamips nodes:

* idlepc: value used for Dynamips optimization (i.e. \`0x80369ac4\`), default is \`0x0\` (no optimization);
* nvram: size of NVRAM in KB, default is \`1024\`;
* slot[0-9]+: the module configured in a specific slot (i.e. \`slot1=NM-1FE-TX\`).

Parameters for QEMU nodes:

* console: can be \`telnet\` or \`vnc\`, default is \`telnet\`;
* cpu: number of configured CPU, default is \`1\`;
* ethernet: number of ethernet interfaces, default is 4;
* uuid: UUID configured, default is a random UUID (i.e. \`641a4800-1b19-427c-ae87-4a8ee90b7790\`).

### Delete an existent lab

\`curl -s -c $COOKIE -b $COOKIE -X DELETE -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%202/Different%20Lab.unl\`

An authenticated user can delete a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X DELETE -H 'Content-type: application/json' http://127.0.0.1/api/labs/Andrea/Folder%202/Different%20Lab.unl | python -m json.tool`
~~~

EOF
