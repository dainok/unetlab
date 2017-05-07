FROM dainok/nodetemplate-qemu:latest
MAINTAINER Andrea Dainese <andrea.dainese@gmail.com>
LABEL author = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL copyright = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL description = "vyos node"
LABEL license = "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
LABEL version = '20170430'

LABEL usage.0 = "docker run -ti --privileged --name node_0 --env CONTROLLER=172.17.0.1 --env LABEL=0 dainok/node-vyos:1.1.7"

ENTRYPOINT ["/sbin/bootstrap.sh"]

# Configuring
RUN mkdir -p /data || exit 1
COPY node /data
