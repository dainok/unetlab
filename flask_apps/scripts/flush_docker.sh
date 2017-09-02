#!/bin/bash

DOCKER="docker -H=tcp://127.0.0.1:4243"
UNUSED_CONTAINER=$(${DOCKER} ps -a -q -f status=exited)
UNUSED_IMAGES=$(${DOCKER} images -a | grep "<none>" | awk '{ print $3 }')

for CONTAINER in "${UNUSED_CONTAINER}"; do
	${DOCKER} rm ${CONTAINER} &> /dev/null
done

for IMAGE in "${UNUSED_IMAGES}"; do
	${DOCKER} rmi ${IMAGE} &> /dev/null
done
