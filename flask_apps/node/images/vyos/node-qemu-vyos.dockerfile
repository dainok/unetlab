FROM dainok/nodetemplate-qemu:latest
MAINTAINER Andrea Dainese <andrea.dainese@gmail.com>
LABEL author = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL copyright = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL description = "vyos node"
LABEL license = "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
LABEL version = '20170430'

#ENTRYPOINT ["/sbin/bootstrap.sh"]

# Configuring
RUN mkdir -p /data || exit 1
COPY node /data
