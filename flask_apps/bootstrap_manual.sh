#!/bin/bash

if [ ! -d /data/logs ]; then
	mkdir /data/logs || exit 1
fi

# Starting SSH
if [ ! -f /etc/ssh/ssh_host_rsa_key ] ; then
	ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa || exit 1
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
/usr/sbin/sshd -D -p 2222 &> /data/logs/sshd.log &
SSHD_PID=$!

# Starting MariaDB
if [ ! -d /data/database/mysql ]; then
	/usr/bin/mysql_install_db --datadir="/data/database" --user="mysql" &> /data/logs/mysql_install_db.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to initialize MariaDB"
		cat /data/logs/mysql_install_db.log
		exit 1
	fi
fi
mkdir -m 755 -p /run/mysqld || exit 1
chown mysql:root /run/mysqld || exit 1
/usr/bin/mysqld --basedir=/usr --datadir=/data/database --plugin-dir=/usr/lib/mysql/plugin --user=mysql --pid-file=/run/mysqld/mysqld.pid --socket=/run/mysqld/mysqld.sock --port=3306 &> /data/logs/mysqld.log &
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
	echo "DROP DATABASE test;" | /usr/bin/mysql -u root &> /data/logs/mysqld.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to delete database \"test\""
		cat /data/logs/mysqld
		exit 1
	fi
fi
if [ ! -d /data/database/unetlab ]; then
	echo "CREATE DATABASE unetlab;" | /usr/bin/mysql -u root &> /data/logs/mysqld.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to create database \"unetlab\""
		cat /data/logs/mysqld.log
		exit 1
	fi
	echo "CREATE USER 'unetlab'@'localhost' IDENTIFIED BY 'UNetLabv2!'" | /usr/bin/mysql -u root &> /data/logs/mysqld.log
	echo "GRANT ALL PRIVILEGES ON unetlab.* TO 'unetlab'@'localhost';" | /usr/bin/mysql -u root &> /data/logs/mysqld.log
	echo "FLUSH PRIVILEGES;" | /usr/bin/mysql -u root &> /data/logs/mysqld.log
	echo "10000000" > /data/database/version
fi

# Starting Memcached
/usr/bin/memcached -m 64 -p 11211 -u memcached -l 127.0.0.1 &> /data/logs/memcached.log &
MEMCACHED_PID=$!

# Starting Redis
/usr/bin/redis-server &> /data/logs/redis.log &
REDIS_PID=$!

# Starting NGINX
if [ ! -f /etc/ssl/api.key ] || [ ! -f /etc/ssl/api.crt ]; then
	rm -f /etc/ssl/api.key /etc/ssl/api.crt || exit 1
	openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 -subj "/C=IT/ST=Italy/L=Padova/O=UNetLab/CN=unl01.example.com" -keyout /etc/ssl/api.key -out /etc/ssl/api.crt || exit 1
fi
mkdir -m 755 -p /run/nginx || exit 1
chown nginx:root /run/nginx || exit 1
/usr/sbin/nginx &> /data/logs/nginx.log &
NGINX_PID=$!

# Starting Celery
/usr/bin/run_controller.py runcelery &> /data/logs/celery.log &
CELERY_PID=$!

# Starting API
/usr/bin/run_controller.py runserver &> /data/logs/api.log &
API_PID=$!

echo ${MARIADB_PID} ${MEMCACHED_PID} ${NGINX_PID} ${API_PID} ${CELERY_PID} ${SSHD_PID} ${REDIS_PID}

echo "Exiting..."

