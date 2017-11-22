#!/bin/bash

export EASYRSA_SSL_CONF=/usr/share/easy-rsa/openssl-1.0.cnf

function controllerStop() {
    echo -n "Shutting down..."
    killall -s SIGTERM mysqld memcached nginx python3 &> /dev/null
    # Double check for critical processes
	while pgrep -f "celery|mysqldi" &> /dev/null; do
        echo -n "."
        sleep 1
    done
    echo " done"
}

echo "Starting controller..."

trap controllerStop SIGHUP SIGINT SIGTERM

if [ ! -d /data/logs ]; then
	mkdir -p /data/logs || exit 1
fi

if [ ! -f /data/pki/.build-completed ]; then
	/usr/share/easy-rsa/easyrsa --pki-dir=/data/pki --batch init-pki || exit 1
	/usr/share/easy-rsa/easyrsa --pki-dir=/data/pki --batch build-ca nopass || exit 1
	/usr/share/easy-rsa/easyrsa --pki-dir=/data/pki --batch gen-dh || exit 1
	cp -a /usr/share/easy-rsa/x509-types/ /data/pki/ || exit 1
	/usr/share/easy-rsa/easyrsa --pki-dir=/data/pki build-server-full controller nopass || exit 1
	/usr/share/easy-rsa/easyrsa --pki-dir=/data/pki build-server-full client_admin nopass || exit 1
	touch /data/pki/.build-completed
fi

if [ ! -d /data/repositories/local ]; then
	mkdir -p /data/repositories/local || exit 1
	git -C /data/repositories/local init || exit 1
fi

# Starting SSH
if [ ! -f /etc/ssh/ssh_host_rsa_key ] ; then
	ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa || exit 1
	sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
	echo "root:UNetLabv2!" | chpasswd
fi
if [ ! -f /etc/ssh/ssh_host_dsa_key ]; then
	ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa || exit 1
fi
if [ ! -f /etc/ssh/ssh_host_ecdsa_key ]; then
	ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa || exit 1
fi
if [ ! -f /etc/ssh/ssh_host_ed25519_key ]; then
	ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519 || exit 1
fi
/usr/sbin/sshd -D -p 2222 &>> /data/logs/sshd.log &
SSHD_PID=$!

# Starting MariaDB
if [ ! -d /data/database/mysql ]; then
	/usr/bin/mysql_install_db --datadir="/data/database" --user="mysql" &>> /data/logs/mysql_install_db.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to initialize MariaDB"
		cat /data/logs/mysql_install_db.log
		exit 1
	fi
fi
mkdir -m 755 -p /run/mysqld || exit 1
chown mysql:root /run/mysqld || exit 1
/usr/bin/mysqld --basedir=/usr --datadir=/data/database --plugin-dir=/usr/lib/mysql/plugin --user=mysql --pid-file=/run/mysqld/mysqld.pid --socket=/run/mysqld/mysqld.sock --port=3306 &>> /data/logs/mysqld.log &
MARIADB_PID=$!
TIMEOUT=10
# Waiting for the DB coming up
while [ ${TIMEOUT} -gt 0 ]; do
	mysqladmin -u root status &> /dev/null
	if [ $? -eq 0 ]; then
		break
	fi
done
mysqladmin -u root status
if [ $? -ne 0 ]; then
	echo " failed"
	echo "ERROR: DB is not coming up"
	exit 1
fi

# Creating and upgrading database
if [ -d /data/database/test ]; then
	echo "DROP DATABASE test;" | /usr/bin/mysql -u root &>> /data/logs/mysqld.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to delete database \"test\""
		cat /data/logs/mysqld
		exit 1
	fi
fi
if [ ! -d /data/database/unetlab ]; then
	echo "CREATE DATABASE unetlab;" | /usr/bin/mysql -u root &>> /data/logs/mysql_install_db.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to create database \"unetlab\""
		cat /data/logs/mysqld.log
		exit 1
	fi
	echo "CREATE USER 'unetlab'@'localhost' IDENTIFIED BY 'UNetLabv2!'" | /usr/bin/mysql -u root &>> /data/logs/mysql_install_db.log
	echo "GRANT ALL PRIVILEGES ON unetlab.* TO 'unetlab'@'localhost';" | /usr/bin/mysql -u root &>> /data/logs/mysql_install_db.log
	echo "FLUSH PRIVILEGES;" | /usr/bin/mysql -u root &>> /data/logs/mysql_install_db.log
	echo "10000000" > /data/database/version
	/usr/bin/run_controller.py db init &>> /data/logs/mysql_install_db.log
fi

# Starting Memcached
/usr/bin/memcached -m 64 -p 11211 -u memcached -l 127.0.0.1 &>> /data/logs/memcached.log &
MEMCACHED_PID=$!

# Starting Redis
/usr/bin/redis-server &>> /data/logs/redis.log &
REDIS_PID=$!

# Starting NGINX
if [ ! -f /etc/ssl/api.key ] || [ ! -f /etc/ssl/api.crt ]; then
	rm -f /etc/ssl/api.key /etc/ssl/api.crt || exit 1
	openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 -subj "/C=IT/ST=Italy/L=Padova/O=UNetLab/CN=unl01.example.com" -keyout /etc/ssl/api.key -out /etc/ssl/api.crt || exit 1
fi
mkdir -m 755 -p /run/nginx || exit 1
chown nginx:root /run/nginx || exit 1
/usr/sbin/nginx &>> /data/logs/nginx.log &
NGINX_PID=$!

# Starting Celery
/usr/bin/run_controller.py runcelery &>> /data/logs/celery.log &
CELERY_PID=$!

# Starting API
/usr/bin/run_controller.py runserver &>> /data/logs/api.log &
API_PID=$!

wait ${API_PID}

killall -s SIGTERM ${MARIADB_PID} ${MEMCACHED_PID} ${NGINX_PID} ${API_PID} ${CELERY_PID} ${SSHD_PID} ${REDIS_PID} python3 &> /dev/null
# Double check for critical processes
while pgrep -f "celery|mysqldi" &> /dev/null; do
	sleep 1
done

echo "Exiting..."

