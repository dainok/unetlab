#!/bin/bash
cd $1
pwd
#dd if=/dev/zero of=minidisk bs=1M count=10
#echo -e 'n\np\n1\n\n\nt\ne\nw\n\n' | fdisk  minidisk
#echo ,20,4,\* | sfdisk -D -H 16 -S 63 minidisk 
#losetup -o 32256 /dev/loop0 minidisk
#mkdosfs -s 1 -h 63 -F 16 /dev/loop0
cp /opt/unetlab/scripts/minidisk.bz2 .
bzip2 -d minidisk.bz2
mkdir loopmnt
#mount /dev/loop0 loopmnt
mount -o loop minidisk loopmnt
cp ios_config.txt loopmnt/
sync
umount loopmnt
#losetup -d /dev/loop0
rm -fr loopmnt
