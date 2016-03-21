#!/bin/sh
cd $1
modprobe nbd
for i in $(seq 0 15) 
	do /opt/qemu/bin/qemu-nbd -c /dev/nbd${i} *.qcow2  && break 
done 
mkdir disk
mount /dev/nbd${i}p1 disk
cp startup-config disk/startup-config 
umount disk
/opt/qemu/bin/qemu-nbd -d /dev/nbd${i}
rm -fr disk


