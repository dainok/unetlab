#!/bin/bash

function nodeStop {
	echo -n "Shutting down..."
	killall -s SIGTERM python3 &> /dev/null
}

echo "Starting node_${LABEL}..."

trap nodeStop SIGINT SIGTERM &> /dev/null

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

