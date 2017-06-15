#!/bin/bash

function nodeStop {
	echo -n "Shutting down..."
	killall -s SIGTERM python3 &> /dev/null
}

echo "Starting node_${LABEL}..."

trap nodeStop SIGINT SIGTERM &> /dev/null

curl -k -m 3 -s https://${CONTROLLER}/static/node/wrapper_qemu.py &> /tmp/wrapper_qemu.py || exit 1
chmod 755 /tmp/wrapper_qemu.py || exit 1

