#!/bin/bash

R="\033[0;31m"
Y="\033[1;33m"
G="\033[0;32m"
U="\033[0m"

TMP="$(mktemp -dt unetlab_build_vyos.XXXXXXXXXX)"
LOG="/tmp/unetlab_build_node.log"
REPOSITORY="dainok"
DOCKER="docker -H=tcp://127.0.0.1:4243"

function clean {
	rm -rf ${TMP} node bootstrap.sh &> /dev/null
	pkill qemu &> /dev/null
}

function infoImage {
	echo -e "Found supported image:"
	echo -e " - type: ${TYPE}"
	echo -e " - subtype: ${SUBTYPE}"
	echo -e " - file: ${SOURCE}/${IMAGE}"
	echo -e " - image name: ${NAME}"
	echo -e "Check ${LOG} for progress and errors"
}

trap clean EXIT
rm -f ${LOG}

which qemu-img &> /dev/null
if [ "$1" == "" ]; then
	echo -e "${R}qemu-img not found${U}"
	exit 1
fi

which qemu-system-x86_64 &> /dev/null
if [ "$1" == "" ]; then
	echo -e "${R}qemu-system-x86_64${U}"
	exit 1
fi

if [ "$1" == "" ]; then
	echo -e "${R}Input file not specified${U}"
	exit 1
fi

if [ ! -f "$1" ]; then
	echo -e "${R}Input file ($1) does not exist${U}"
	exit 1
fi

IMAGE=$(basename $1)
SOURCE=$(dirname $1)

if [ ! -f "${SOURCE}/${IMAGE}" ]; then
	echo -e "${R}Input file (${SOURCE}/${IMAGE}) does not exist${U}"
	exit 1
fi

rm -rf node &>> ${LOG} && mkdir -p node/image &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}Cannot create directory (node)${U}"
	exit 1
fi

cp -a ../bootstrap_node.sh bootstrap.sh &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}Cannot find bootstrap file (../bootstrap_node.sh)${U}"
	exit 1
fi

case "${IMAGE}" in
	vyos-*-amd64.iso)
		TYPE="qemu"
		SUBTYPE="vyos"
		DISKS="${TMP}/hda.qcow2"
		NAME="node-${SUBTYPE}:$(echo ${IMAGE} | sed 's/vyos-\([0-9.]*\)-amd64.iso/\1/')"
		infoImage
		qemu-img create -f qcow2 node/image/hda.qcow2 1G &>> ${LOG}
		qemu-system-x86_64 -boot order=c,once=d -cdrom ${SOURCE}/${IMAGE} -hda node/image/hda.qcow2 -enable-kvm -m 1G -serial telnet:0.0.0.0:5023,server,nowait -monitor telnet:0.0.0.0:5024,server,nowait -nographic &>> ${LOG} &
		vyos/preconfigure_${SUBTYPE}.py &>> ${LOG}
		if [ $? -ne 0 ]; then
			echo -e "${R}Preconfiguration failed${U}"
			exit 1
		fi
		;;
	*)
		echo -e "${R}Input file (${SOURCE}/${IMAGE}) is not supported${U}"
		exit 1
		;;
esac

echo -ne "Building Docker image ${REPOSITORY}/${NAME}... "
${DOCKER} build -t ${REPOSITORY}/${NAME} -f ${SUBTYPE}/node-${TYPE}-${SUBTYPE}.dockerfile . &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}failed${U}"
	exit 1
fi
echo -e "${G}done${U}"

rm -f ${LOG}
exit 0
