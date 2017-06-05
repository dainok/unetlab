FROM alpine:latest
MAINTAINER Andrea Dainese <andrea.dainese@gmail.com>
LABEL author = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL copyright = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL description = "Router"
LABEL license = "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
LABEL version = '20170430'

LABEL build = "docker build -t dainok/router:latest -f router.dockerfile ."
LABEL usage.0 = "docker run -d -h router --ip 172.16.0.3 --name router --network workload-net -p 1194:1194 -p 5005:5005 -p 5443:5443 --restart always --env API=zqg81ge585t0bt3qe0sjj1idvw7hv7vfgc11dsq6 --env CONTROLLER=1.1.1.1 --env DOCKERIP=172.16.0.1 --env ROUTERID=0 dainok/router"

ENTRYPOINT ["/sbin/bootstrap.sh"]

# Installing dependencies
RUN apk update || exit 1
RUN apk upgrade || exit 1
RUN apk add bash curl nginx openssl openvpn python3 || exit 1
RUN pip3 install --no-cache-dir --upgrade pip || exit 1

# Configuring
COPY bootstrap_router.sh /sbin/bootstrap.sh

# Cleaning
RUN find /var/cache/apk/ -type f -delete || exit 1
