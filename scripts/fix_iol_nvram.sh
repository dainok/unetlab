#!/bin/bash

if [ ${#} -ne 1 ]; then
    echo 'ERROR: Must need a NVRAM file as argument.'
    exit 1
fi

echo ${1} | egrep '/opt/unetlab/tmp/0/[0-9a-f\-]{36}/[0-9]+/nvram_[0-9]{5}' > /dev/null 2>&1
if [ ${?} -ne 0 ]; then
    echo 'ERROR: File is not valid.'
    exit 2
fi

if [ ! -f ${1} ]; then
    echo 'ERROR: File does not exist.'
    exit 3
fi

NVRAM_FILE=$(echo ${1} | cut -d/ -f 8)
NVRAM_ID=$(echo ${NVRAM_FILE} | sed 's/nvram_[0]\+//')
NODE_ID=$(echo ${1} | cut -d/ -f 7)
NODE_DIR=$(echo ${1} | cut -d/ -f 1-7)

if [ ${NODE_ID} -ne ${NVRAM_ID} ]; then
    mv -f ${1} ${NODE_DIR}/nvram_$(printf "%05i" ${NODE_ID})
fi
exit 0
