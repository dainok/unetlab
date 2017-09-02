
kill -s SIGTERM ${NGINX_PID} &> /dev/null
wait ${NGINX_PID}

echo "Exiting..."

