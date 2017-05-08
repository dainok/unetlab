FROM alpine:latest
MAINTAINER Andrea Dainese <andrea.dainese@gmail.com>
LABEL author = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL copyright = "Andrea Dainese <andrea.dainese@gmail.com>"
LABEL description = "Router"
LABEL license = "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
LABEL version = '20170430'

LABEL build = "docker build -t dainok/router:latest -f router.dockerfile ."
LABEL usage.0 = "docker run --name router_0 --env CONTROLLER=172.17.0.1 --env LABEL=0 dainok/router"

ENTRYPOINT ["/sbin/bootstrap.sh"]

# Installing dependencies
RUN apk update || exit 1
RUN apk upgrade || exit 1
RUN apk add bash curl python3 || exit 1
RUN pip3 install --no-cache-dir --upgrade pip || exit 1

# Configuring
COPY bootstrap_router.sh /sbin/bootstrap.sh

# Cleaning
RUN find /var/cache/apk/ -type f -delete || exit 1
