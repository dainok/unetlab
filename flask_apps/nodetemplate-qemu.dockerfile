FROM alpine:latest
MAINTAINER Andrea Dainese <andrea.dainese@gmail.com>
LABEL author = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL copyright = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL description = "QEMU template node"
LABEL license = "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
LABEL version = '20170430'

LABEL build = "docker build -t dainok/nodetemplate-qemu:latest -f nodetemplate-qemu.dockerfile ."

# Installing dependencies
RUN apk update || exit 1
RUN apk upgrade || exit 1
RUN apk add bash curl iptables python3 qemu-img qemu-system-x86_64 || exit 1
RUN pip3 install --no-cache-dir --upgrade pip || exit 1
RUN pip3 install --no-cache-dir flask_restful pexpect || exit 1

# Configuring
COPY bootstrap_node.sh /sbin/bootstrap.sh

# Cleaning
RUN find /var/cache/apk/ -type f -delete || exit 1
