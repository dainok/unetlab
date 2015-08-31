#!/bin/bash
# vim: syntax=sh tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

clean() {
	IMAGE=$1
	umount ${IMAGE}/vdisk > /dev/null 2>&1
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0 > /dev/null 2>&1
	rmdir ${IMAGE}/vdisk > /dev/null 2>&1
}

export() {
	# Set of script to export config from IMAGE to FILE
	IMAGE=$1
	FILE=$2
	mkdir -p ${IMAGE}/vdisk > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "ERROR: cannot create vdisk directory."
		clean $1
		exit 1
	fi
	/opt/qemu/bin/qemu-nbd -c /dev/nbd0 -r ${IMAGE}/virtioa.qcow2 > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "ERROR: cannot bind IMAGE to /dev/nbd0."
		clean $1
		exit 2
	fi
	mount -t vfat /dev/nbd0p1 ${IMAGE}/vdisk > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "ERROR: cannot mount /dev/nbd0."
		clean $1
		exit 3
	fi
	cp -a ${IMAGE}/vdisk/nvram ${FILE} > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "ERROR: cannot copy nvram to FILE."
		clean $1
		exit 4
	fi
	clean $1
}

import() {
	# Set of script to IMPORT config from FILE to IMAGE
	IMAGE=$1
	FILE=$2
	mkdir -p ${IMAGE}/vdisk > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "ERROR: cannot create vdisk directory."
		clean $1
		exit 5
	fi
	/opt/qemu/bin/qemu-nbd -c /dev/nbd0 ${IMAGE}/virtioa.qcow2 > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "ERROR: cannot bind IMAGE to /dev/nbd0."
		clean $1
		exit 6
	fi
	mount -t vfat /dev/nbd0p1 ${IMAGE}/vdisk > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "ERROR: cannot mount /dev/nbd0."
		clean $1
		exit 7
	fi
	cp -a ${FILE} ${IMAGE}/vdisk/nvram > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "ERROR: cannot copy nvram to FILE."
		clean $1
		exit 8
	fi
	clean $1
}

case $1 in
	"import")
		import $2 $3
		;;
	"export")
		export $2 $3
		;;
	*)
		echo "ERROR: invalid action."
		exit 9
		;;
esac
exit 0
