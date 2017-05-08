#!/bin/bash

function nodeStop {
	echo -n "Shutting down..."
	killall -s SIGTERM python3 &> /dev/null
}

echo "Starting node_${LABEL}..."

trap nodeStop SIGINT SIGTERM &> /dev/null

curl -m 3 -s http://${CONTROLLER}:5000/static/node/wrapper_qemu.py &> /tmp/wrapper_qemu.py || exit 1
chmod 755 /tmp/wrapper_qemu.py || exit 1

