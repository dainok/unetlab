#!/bin/bash
URL="https://${CONTROLLER}/api/v1/bootstrap/nodes/${LABEL}"
PID=0

function nodeStop {
	echo -n "Shutting down..."
	killall -s SIGTERM curl sleep &> /dev/null
	if [ ${PID} -ne 0 ]; then
		kill -SIGTERM ${PID}
		wait ${PID}
	fi
	echo " done"
}

echo "Starting node..."

trap nodeStop SIGINT SIGTERM SIGHUP

while true; do
    curl -k -m 3 -s "${URL}" &> /tmp/init
    if [ $? -ne 0 ]; then
        echo "ERROR: cannot download init script from ${URL}"
        sleep 5
    else
        break
    fi
done

bash /tmp/init &
PID=$!
wait $PID
exit $?

echo "Exiting..."

