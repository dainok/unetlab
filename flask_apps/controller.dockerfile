FROM alpine:latest
MAINTAINER Andrea Dainese <andrea.dainese@gmail.com>
LABEL author = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL copyright = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL description = "The API and controller module"
LABEL license = "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
LABEL version = "20170320"

LABEL build = "docker build -t dainok/controller:latest -f controller.dockerfile ."
LABEL usage.0 = "docker volume create --name controller_data"
LABEL usage.1 = "docker run -ti --rm --name controller --volume controller_data:/data dainok/controller /sbin/bootstrap.sh"

#ENTRYPOINT ["/sbin/bootstrap.sh"]
EXPOSE :80 :443 :5005

# Installing dependencies
RUN apk update || exit 1
RUN apk upgrade || exit 1
RUN apk add bash gcc git libc-dev mariadb mariadb-client mariadb-dev memcached nginx openssh python3 python3-dev || exit 1
RUN pip3 install --no-cache-dir --upgrade pip || exit 1
RUN pip3 install --no-cache-dir celery Flask-MySQLdb Flask-SQLAlchemy flask_migrate flask_restful python3-memcached sh || exit 1

# Configuring
RUN mkdir /usr/lib/python3.5/site-packages/controller || exit 1
RUN git config --global user.email "root@example.com" || exit 1
RUN git config --global user.name "Root User"
COPY nginx.conf /etc/nginx/
COPY run_controller.py /usr/bin
COPY controller /usr/lib/python3.5/site-packages/controller
COPY controller /root
COPY bootstrap.sh /sbin/bootstrap.sh

# Cleaning
RUN find /var/cache/apk/ -type f -delete || exit 1
