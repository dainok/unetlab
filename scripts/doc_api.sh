#!/bin/bash

COOKIE=/tmp/cookie

cat << EOF > /usr/src/unetlab.github.io/_posts/2015-09-01-using-uNetlab-apis.md
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
* unauthorized for 401 HTTP code, meaning that user should login;
* forbidden for 403 HTTP code, meaning that user does not have enough privileges;
* fail for other 40x HTTP codes;
* error for 50x HTTP codes.

The default Web-UI uses only APIs, so this is an essential part to develop new Web-UI themes, integration and so on.
Mind that each user can login from a single location only. If the same user login twice, the second login disable the first one.

## Authentication

The following API requests are involved on login and logout process. All other API requests require an authenticated user.

### Login

\`curl -s -b $COOKIE -c $COOKIE -X POST -d '{"username":"admin","password":"unl"}' http://127.0.0.1/api/auth/login\`

A successful login provides the following output:

~~~
`curl -s -b $COOKIE -c $COOKIE -X POST -d '{"username":"admin","password":"unl"}' http://127.0.0.1/api/auth/login | python -m json.tool`
~~~

### User Info

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/auth\`

An authenticated user can get its own information:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/auth | python -m json.tool`
~~~

### Logout

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/auth/logout\`

All users can logout, this request cannot fail:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/auth/logout | python -m json.tool`
~~~
`curl -s -b $COOKIE -c $COOKIE -X POST -d '{"username":"admin","password":"unl"}' http://127.0.0.1/api/auth/login > /dev/null`
## System status

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/status\`

An authenticated user can get system statistics:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/status | python -m json.tool`
~~~

## List node templates

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/list/templates/\`

An authenticated user can list all available node templates:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/list/templates/ | python -m json.tool`
~~~

A single template can be listed:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/list/templates/iol\`

All available images for the selected template will be included in the output:

`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/list/templates/iol | python -m json.tool`

## List network types

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/list/networks\`

An authenticated user can list all available network types:

`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/list/networks | python -m json.tool`

## Navigating between folders

The following API requests allow to manages folders and labs as files.

### List content inside a folder

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/folders/\`

An authenticated user can list what is inside a folder:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/folders/ | python -m json.tool`
~~~

Folders and labs are listed using different arrays.

### Add a new folder

\`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"path":"/Folder 3","name":"New Folder"}' -H "Content-type: application/json" http://127.0.0.1/api/folders\`

An authenticated user can add a folder inside a specific path:

~~~
`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"path":"/Folder 3","name":"New Folder"}' -H "Content-type: application/json" http://127.0.0.1/api/folders | python -m json.tool`
~~~

### Delete an existing folder

\`curl -s -c $COOKIE -b $COOKIE -X DELETE -H "Content-type: application/json" http://127.0.0.1/api/folders/Folder%203/New%20Folder\`

An authenticated user can delete an existing folder:

~~~
`curl -s -c $COOKIE -b $COOKIE -X DELETE -H "Content-type: application/json" http://127.0.0.1/api/folders/Folder%203/New%20Folder | python -m json.tool`
~~~

## Managing labs

The following API requests allow to manage labs and object inside a lab, like nodes, networks... and so on.

### Get a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl\`

An authenticated user can retrieve a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl | python -m json.tool`
~~~

### Get one or all networks configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/networks\`

An authenticated user can retrieve all configured networks in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/networks | python -m json.tool`
~~~

A single network can be retrieved:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/networks/1\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/networks/1 | python -m json.tool`
~~~

### Get all remote endpoint for both ethernet and serial interfaces

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/links\`

An authenticated user can retrieve all available endpoint in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/links | python -m json.tool`
~~~

This API is useful when a user need to connect a node.

### Get one or all nodes configured in a lab

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/nodes\`

An authenticated user can retrieve all configured nodes in a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/nodes | python -m json.tool`
~~~

A single node can be retrieved:

\`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/nodes/1\`

Here the output:

~~~
`curl -s -c $COOKIE -b $COOKIE -X GET -H "Content-type: application/json" http://127.0.0.1/api/labs/Lab%201.unl/nodes/1 | python -m json.tool`
~~~

### Create a new lab

\`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"path":"/Folder 3","name":"New Lab","version":"1","author":"Andrea Dainese","description":"a new demo lab"}' -H "Content-type: application/json" http://127.0.0.1/api/labs\`

An authenticated user can create a new lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X POST -d '{"path":"/Folder 3","name":"New Lab","version":"1","author":"Andrea Dainese","description":"a new demo lab"}' -H "Content-type: application/json" http://127.0.0.1/api/labs | python -m json.tool`
~~~

### Delete an existent lab

\`curl -s -c $COOKIE -b $COOKIE -X DELETE -H "Content-type: application/json" http://127.0.0.1/api/labs/Folder%203/New%20Lab.unl\`

An authenticated user can delete a lab:

~~~
`curl -s -c $COOKIE -b $COOKIE -X DELETE -H "Content-type: application/json" http://127.0.0.1/api/labs/Folder%203/New%20Lab.unl | python -m json.tool`
~~~

EOF
