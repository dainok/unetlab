#!/bin/bash
URL="https://${CONTROLLER}/api/v1/bootstrap/routers/${ROUTERID}?api_key=${API}"
PID=0

function routerStop {
	echo -n "Shutting down..."
	killall -s SIGTERM curl sleep &> /dev/null
	if [ ${PID} -ne 0 ]; then
		kill -SIGTERM ${PID}
		wait ${PID}
	else
		exit
	fi
}

echo "Starting router..."

trap routerStop SIGINT SIGTERM

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
if [ ${PID} -ne 0 ]; then
	echo waiting
	wait $PID
	exit $?
fi

echo "Exiting..."

