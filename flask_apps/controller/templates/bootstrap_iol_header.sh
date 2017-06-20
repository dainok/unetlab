#!/bin/bash

function nodeExit {
	curl -k -s -o /dev/null -X PATCH -d "{\"ip\":null,\"state\":\"off\"}" -H 'Content-type: application/json' "https://${CONTROLLER}/api/v1/nodes/${LABEL}?api_key=${API}" || exit 1
}

function nodeStop {
	echo -n "Shutting down..."
	killall -s SIGTERM python3 &> /dev/null
}

trap nodeStop SIGINT SIGTERM &> /dev/null
trap nodeExit EXIT &> /dev/null

# Registering router
echo -n "Registering node_${LABEL}..."
IP_ADDRESS=$(ifconfig eth0 | grep "inet addr" | sed 's/.*inet addr:\([0-9.]*\) .*/\1/g')
curl -k -s -o /dev/null -X PATCH -d "{\"ip\":null,\"state\":\"off\"}" -H 'Content-type: application/json' "https://${CONTROLLER}/api/v1/nodes/${LABEL}?api_key=${API}" || exit 1

echo "Starting node_${LABEL}..."

curl -k -m 3 -s https://${CONTROLLER}/static/node/wrapper_iol.py &> /tmp/wrapper_iol.py || exit 1
chmod 755 /tmp/wrapper_iol.py || exit 1

HOSTNAME=$(cat /data/node/iourc | grep "=" | head -n1 | sed 's/\ *=.*$//')
hostname ${HOSTNAME}
fgrep '127.0.1.1' &> /dev/null
if [ $? -ne 0 ]; then
	echo -e "127.0.1.1\t${HOSTNAME}" >> /etc/hosts
fi
fgrep "xml.cisco.com" /etc/hosts &> /dev/null
if [ $? -ne 0 ]; then
	echo -e "127.0.0.127\txml.cisco.com" >> /etc/hosts
fi

