#!/bin/bash

function routerStop {
	echo -n "Shutting down..."
	kill -s SIGTERM ${ROUTER_PID} ${NGINX_PID} &> /dev/null
	killall -s SIGTERM nginx openssl python3 &> /dev/null
	echo " done"
}

function routerReload {
	SERVER_ACTIVE=true
	kill -s SIGHUP ${ROUTER_PID} &> /dev/null
}

SERVER_ACTIVE=true

trap routerStop SIGINT SIGTERM &> /dev/null
trap routerReload SIGHUP &> /dev/null

# Registering router
echo -n "Registering  router ${ROUTERID}..."
IP_ADDRESS=$(ifconfig eth0 | grep "inet addr" | sed 's/.*inet addr:\([0-9.]*\) .*Mask:/\1\//g')
curl -k -s -o /dev/null -X POST -d "{\"id\":${ROUTERID},\"inside_ip\":\"${IP_ADDRESS}\"}" -H 'Content-type: application/json' "https://${CONTROLLER}/api/v1/routers?api_key=${API}" || exit 1
echo "done"

echo -n "Starting router ${ROUTERID}..."


if [ ! -d /data/logs ]; then
    mkdir -p /data/logs || exit 1
fi

# Starting NGINX
echo -n "admin:" > /etc/nginx/.htpasswd
echo -n "${API}" | openssl passwd -apr1 -stdin >> /etc/nginx/.htpasswd
cat << EOF > /etc/nginx/nginx.conf
# /etc/nginx/nginx.conf

user nginx;
daemon off;
worker_processes auto;
pcre_jit on;
error_log /data/logs/nginx_error.log warn;

events {
	worker_connections 1024;
}

http {
	include /etc/nginx/mime.types;
	default_type application/octet-stream;
	server_tokens off;
	client_max_body_size 0;
	keepalive_timeout 65;
	sendfile on;
	tcp_nodelay on;
	log_format main '\$remote_addr - \$remote_user [\$time_local] "\$request" '
					'\$status \$body_bytes_sent "\$http_referer" '
					'"\$http_user_agent" "\$http_x_forwarded_for"';
	access_log /data/logs/nginx_access.log main;

	server {
		listen 5443 default_server ssl;
		listen [::]:5443 default_server ssl;

		ssl on;
		ssl_certificate cert.pem;
		ssl_certificate_key cert.key;
				
		location /docker/ {
			proxy_pass http://${DOCKERIP}:4243/;
			auth_basic "UNetLab Router Node";
			auth_basic_user_file /etc/nginx/.htpasswd;
		}
		location ~ /nodes/(?<node_ip>[^/]+)/? {
			rewrite ^.*\/nodes\/(?<node_ip>[^\/]+)\/?(.*) /\$2 break;
			proxy_pass http://\$node_ip:5000/\$2;
			auth_basic "UNetLab Router Node";
			auth_basic_user_file /etc/nginx/.htpasswd;
		}
		location / {
			deny all;
		}
	}
}
EOF
if [ ! -f /etc/nginx/cert.key ]; then
	openssl req -x509 -newkey rsa:4096 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.pem -days 3650 -nodes -subj "/C=IT/ST=Italy/L=Padova/O=RR Labs/CN=127.0.0.1" || exit 1
fi
mkdir -m 755 -p /run/nginx &> /dev/null
chown nginx:root /run/nginx &> /dev/null
/usr/sbin/nginx &>> /data/logs/nginx.log &
NGINX_PID=$!

# Starting router
curl -k -m 3 -s https://${CONTROLLER}/static/router/router.py &> /tmp/router.py || exit 1
curl -k -m 3 -s https://${CONTROLLER}/static/router/router_modules.py &> /tmp/router_modules.py || exit 1
chmod 755 /tmp/router.py || exit 1
cd /tmp || exit 1
./router.py -d -c ${CONTROLLER} -i ${ROUTERID} -k ${API} &>> /data/logs/router.log &
ROUTER_PID=$!

echo " done"

while ${SERVER_ACTIVE}; do
	SERVER_ACTIVE=false
	wait ${ROUTER_PID}
done

echo ${ROUTER_PID}

