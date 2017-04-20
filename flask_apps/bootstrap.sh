#!/bin/bash

shutdown() {
	echo -n "Shutting down..."
	killall -s SIGTERM mysqld memcached nginx pytyon3 &> /data/logs/shutdown.log
	# Double check for critical processes
	while pgrep mysqld &> /dev/null; do
		echo -n "."
		sleep 1
	done
	echo " done"
}

echo -n "Starting controller..."

trap shutdown SIGHUP SIGINT SIGTERM &> /dev/null

if [ ! -d /data/logs ]; then
	mkdir /data/logs || exit 1
fi

# Starting MariaDB
if [ ! -d /data/database/mysql ]; then
	/usr/bin/mysql_install_db --datadir="/data/database" --user="mysql" &> /data/logs/mariadb_install.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to initialize MariaDB"
		cat /data/logs/mysql_install_db.log
		exit 1
	fi
fi
mkdir -m 755 -p /run/mysqld &> /dev/null
chown mysql:root /run/mysqld &> /dev/null
/usr/bin/mysqld --basedir=/usr --datadir=/data/database --plugin-dir=/usr/lib/mysql/plugin --user=mysql --pid-file=/run/mysqld/mysqld.pid --socket=/run/mysqld/mysqld.sock --port=3306 &> /data/logs/mariadb.log &
MARIADB_PID=$!
TIMEOUT=10
# Waiting for the DB coming up
while [ ${TIMEOUT} -gt 0 ]; do
	mysqladmin -u root status &> /dev/null
	if [ $? -eq 0 ]; then
		break
	fi
done
mysqladmin -u root status &> /dev/null
if [ $? -ne 0 ]; then
	echo " failed"
	echo "ERROR: DB is not coming up"
	exit 1
fi

# Creating and upgrading database
if [ -d /data/database/test ]; then
	echo "DROP DATABASE test;" | /usr/bin/mysql -u root &> /data/logs/mariadb_database.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to delete database \"test\""
		exit 1
	fi
fi
if [ ! -d /data/database/unetlab ]; then
	echo "CREATE DATABASE unetlab;" | /usr/bin/mysql -u root &> /data/logs/mariadb_database.log
	if [ $? -ne 0 ]; then
		echo " failed"
		echo "ERROR: failed to create database \"unetlab\""
		exit 1
	fi
	echo "10000000" > /data/database/version
fi
for SCHEMA in $(ls -1 /etc/unetlab/schema-*.sql); do
	VERSION=$(cat /data/database/version | sed 's/schema-\([0-9]*\)\.sql/\1/g')
	SCHEMA_VERSION=$(echo ${SCHEMA} | sed 's/.*\/schema-\([0-9]*\)\.sql/\1/g')
	if [ ${VERSION} -lt ${SCHEMA_VERSION} ]; then
		mysql -u root unetlab < ${SCHEMA}
		if [ $? -ne 0 ]; then
			echo " failed"
			echo "ERROR: failed to upgrade database to ${SCHEMA_VERSION}"
			exit 1
		fi
		echo ${SCHEMA_VERSION} > /data/database/version
	fi
done

# Starting Memcached
/usr/bin/memcached -m 64 -p 11211 -u memcached -l 127.0.0.1 &> /data/logs/memcached.log &
MEMCACHED_PID=$!

# Starting NGINX
mkdir -m 755 -p /run/nginx &> /dev/null
chown nginx:root /run/nginx &> /dev/null
/usr/sbin/nginx &> /data/logs/nginx.log &
NGINX_PID=$!

# Starting API
mkdir -m 755 -p /data/etc &> /dev/null
/usr/bin/api.py &> /data/logs/api.log &
API_PID=$!

echo " done"

wait ${MARIADB_PID} ${MEMCACHED_PID} ${NGINX_PID} ${API_PID}

echo "Exiting..."
