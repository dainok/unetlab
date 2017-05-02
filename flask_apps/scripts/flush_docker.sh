#!/bin/bash

DOCKER="docker -H=tcp://127.0.0.1:4243"
UNUSED_CONTAINER=$(${DOCKER} ps -a -q -f status=exited)
UNUSED_IMAGES=$(${DOCKER} images -a | grep "^<none>" | awk '{ print $3 }')

if [ "${UNUSED_CONTAINER}" != "" ]; then
	${DOCKER} rm ${UNUSED_CONTAINER} &> /dev/null
fi
if [ "${UNUSED_IMAGES}" != "" ]; then
	${DOCKER} rmi ${UNUSED_IMAGES} &> /dev/null
fi
