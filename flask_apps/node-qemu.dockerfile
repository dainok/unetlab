FROM alpine:latest
MAINTAINER Andrea Dainese <andrea.dainese@gmail.com>
LABEL author = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL copyright = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL description = "QEMU node"
LABEL license = "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
LABEL version = '20170430'

LABEL build = "docker build -t dainok/node-qemu:latest -f node-qemu.dockerfile ."
LABEL usage.0 = "docker run --privileged -ti --rm --name node_0 dainok/node-qemu /sbin/bootstrap.sh"

#ENTRYPOINT ["/sbin/bootstrap.sh"]

# Installing dependencies
RUN apk update || exit 1
RUN apk upgrade || exit 1
RUN apk add bash qemu-img qemu-system-x86_64qemu-system-x86_64 || exit 1
#RUN pip3 install --no-cache-dir --upgrade pip || exit 1
#RUN pip3 install --no-cache-dir celery Flask-MySQLdb Flask-SQLAlchemy flask_migrate flask_restful python3-memcached sh || exit 1

# Configuring
RUN mkdir -p /data/node
#RUN mkdir /usr/lib/python3.5/site-packages/controller || exit 1
#RUN git config --global user.email "root@example.com" || exit 1
#RUN git config --global user.name "Root User"
#COPY nginx.conf /etc/nginx/
#COPY run_controller.py /usr/bin
#COPY controller /usr/lib/python3.5/site-packages/controller
#COPY controller /root
#COPY bootstrap.sh /sbin/bootstrap.sh
# node
# docker cp vyos-1.1.7-amd64.iso.asc node_0:/data/node

# mkdir -p /data/node
# # qemu-img create -f qcow2 /data/node/hda.qcow2 1G
# mv /tmp/vyos-1.1.7-amd64.iso /data/node/
# qemu-system-x86_64 -boot d -cdrom /data/node/vyos-1.1.7-amd64.iso -hda /data/node/hda.qcow2 -enable-kvm -m 1G -serial telnet:0.0.0.0:5023,server,nowait


# Cleaning
RUN find /var/cache/apk/ -type f -delete || exit 1
