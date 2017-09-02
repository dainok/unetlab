#!/bin/bash

function nodeExit {
	curl -k -s -o /dev/null -X PATCH -d "{\"ip\":\"0.0.0.0\",\"state\":\"off\"}" -H 'Content-type: application/json' "https://${CONTROLLER}/api/v1/nodes/${LABEL}?api_key=${API}" || exit 1
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
curl -k -s -o /dev/null -X PATCH -d "{\"ip\":\"${IP_ADDRESS}\",\"state\":\"off\"}" -H 'Content-type: application/json' "https://${CONTROLLER}/api/v1/nodes/${LABEL}?api_key=${API}" || exit 1

echo "Starting node_${LABEL}..."

curl -k -m 3 -s https://${CONTROLLER}/static/node/wrapper_qemu.py &> /tmp/wrapper_qemu.py || exit 1
chmod 755 /tmp/wrapper_qemu.py || exit 1

