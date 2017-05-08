#!/bin/bash
URL=http://${CONTROLLER}:5000/api/v1/bootstrap/routers/${ID}
PID=0

function routerStop {
	if [ ${PID} -ne 0 ]; then
		kill -SIGTERM ${PID}
		wait ${PID}
	fi
}

curl -m 3 -s ${URL} &> /tmp/init
if [ $? -ne 0 ]; then
	echo "ERROR: cannot download init script from ${URL}"
	exit 1
fi

trap routerStop SIGINT SIGTERM
bash /tmp/init &
PID=$!
wait $PID
exit $?

