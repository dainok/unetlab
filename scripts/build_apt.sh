#!/bin/bash
BUILD_DIR="/build"

# Building the repository
cd ${BUILD_DIR}/apt
mkdir -p ${BUILD_DIR}/apt/dists/trusty/rrlabs/binary-amd64 ${BUILD_DIR}/apt/dists/trusty/rrlabs/binary-i386 
dpkg-scanpackages -a amd64 -m pool > ${BUILD_DIR}/apt/dists/trusty/rrlabs/binary-amd64/Packages
gzip -c ${BUILD_DIR}/apt/dists/trusty/rrlabs/binary-amd64/Packages > ${BUILD_DIR}/apt/dists/trusty/rrlabs/binary-amd64/Packages.gz
dpkg-scanpackages -a i386 -m pool > ${BUILD_DIR}/apt/dists/trusty/rrlabs/binary-i386/Packages
gzip -c ${BUILD_DIR}/apt/dists/trusty/rrlabs/binary-i386/Packages > ${BUILD_DIR}/apt/dists/trusty/rrlabs/binary-i386/Packages.gz
apt-ftparchive release ${BUILD_DIR}/apt/dists/trusty > ${BUILD_DIR}/apt/dists/trusty/Release
rm -f ${BUILD_DIR}/apt/dists/trusty/InRelease ${BUILD_DIR}/apt/dists/trusty/Release.gpg
gpg --clearsign -o ${BUILD_DIR}/apt/dists/trusty/InRelease ${BUILD_DIR}/apt/dists/trusty/Release
gpg -abs -o ${BUILD_DIR}/apt/dists/trusty/Release.gpg ${BUILD_DIR}/apt/dists/trusty/Release
