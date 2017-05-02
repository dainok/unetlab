#!/bin/bash
URL=http://${CONTROLLER}:5000/api/v1/bootstrap/${LABEL}
PID=0

function nodeStop {
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

trap nodeStop SIGINT SIGTERM
bash /tmp/init &
PID=$!
wait $PID
exit $?

