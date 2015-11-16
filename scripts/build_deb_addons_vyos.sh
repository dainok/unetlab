#!/bin/bash
# Vars
CONTROL="/usr/src/unetlab/debian/addons_vyos_control.template"
SRC_DIR="/usr/src/unetlab"
BUILD_DIR="/build"
CONTROL_DIR="$(mktemp -dt)"
DATA_DIR="$(mktemp -dt)"
ARCH=$(cat ${CONTROL} | grep Architecture | sed 's/[A-Za-z]\+: //')
VERSION="$(cat ${CONTROL} | grep Version | sed 's/^[A-Za-z]\+: \([0-9\.]\+\)-\([0-9]\+\)/\1/')"
RELEASE="$(cat ${CONTROL} | grep Version | sed 's/^[A-Za-z]\+: \([0-9\.]\+\)-\([0-9]\+\)/\2/')"
PACKAGE="$(cat ${CONTROL} | grep Package | sed 's/^[A-Za-z]\+: //')"

# Prepare the environment
mkdir -p ${DATA_DIR}/opt/unetlab/addons/qemu
cp -a /opt/unetlab/addons/qemu/vyos-1.1.6-amd64 ${DATA_DIR}/opt/unetlab/addons/qemu

# Building the package
cat ${CONTROL} | sed "s/%VERSION%/${VERSION}/" | sed "s/%RELEASE%/${RELEASE}/" > ${CONTROL_DIR}/control
cd ${DATA_DIR}
tar czf data.tar.gz *
find -type f -exec md5sum {} \; >> ${CONTROL_DIR}/md5sums
echo 2.0 > ${CONTROL_DIR}/debian-binary
cd ${CONTROL_DIR}
tar czf control.tar.gz md5sums control
cd ${SRC_DIR}
mkdir -p ${BUILD_DIR}/apt/pool/trusty/u/${PACKAGE}
ar -cr ${BUILD_DIR}/apt/pool/trusty/u/${PACKAGE}/${PACKAGE}_${VERSION}-${RELEASE}_${ARCH}.deb ${CONTROL_DIR}/debian-binary ${CONTROL_DIR}/control.tar.gz ${DATA_DIR}/data.tar.gz
rm -rf ${CONTROL_DIR} ${DATA_DIR}
