#!/bin/bash

if [ $# -ne 1 ]; then
	echo "ERROR: must specify destination file."
	exit 1
fi

DESTINATION=$1
TEMP=$(mktemp -d --suffix=_unetlab)
VMDK="Unified_Networking_Lab-disk1.vmdk"
QCOW="Unified_Networking_Lab-disk1.qcow2"
OVF="Unified Networking Lab.ovf"

echo -ne "Creating a VMDK disk under $TEMP... "
/opt/qemu/bin/qemu-img create -f vmdk $TEMP/unetlab-disk1.vmdk 20G > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Binding VMDK disk under /dev/nbd0... "
/opt/qemu/bin/qemu-nbd -c /dev/nbd0 $TEMP/unetlab-disk1.vmdk > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Partitioning /dev/nbd0... "
sfdisk /dev/nbd0 << EOF > /dev/null 2>&1
unit: sectors

/dev/nbd0p1 : start=     2048, size=   497664, Id=83, bootable
/dev/nbd0p2 : start=   499712, size= 41443328, Id=8e
/dev/nbd0p3 : start=        0, size=        0, Id= 0
/dev/nbd0p4 : start=        0, size=        0, Id= 0
EOF
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Formatting /dev/nbd0p1... "
mkfs -t ext4 /dev/nbd0p1 > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Tuning /dev/nbd0p1..."
tune2fs -c0 -i0 /dev/nbd0p1 > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Creating PV on /dev/nbdp2..."
pvcreate /dev/nbd0p2 > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Creating VG on /dev/nbdp2..."
vgcreate unlvg /dev/nbd0p2 > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Creating LV on VG..."
lvcreate -l 100%FREE -n rootvol unlvg
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Formatting /dev/unlvg/rootvol "
mkfs -t ext4 /dev/unlvg/rootvol > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Tuning /dev/unlvg/rootvol"
tune2fs -c0 -i0 /dev/unlvg/rootvol > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

mkdir $TEMP/target

echo -ne "Mounting /dev/unlvg/rootvol on $TEMP/target..."
mount /dev/unlvg/rootvol $TEMP/target > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

mkdir $TEMP/target/boot

echo -ne "Mounting /dev/nbd0p1 on $TEMP/target/boot..."
mount /dev/nbd0p1 $TEMP/target/boot > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	umount $TEMP/target
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -e "Installing Ubuntu under $TEMP/target..."
debootstrap --arch=amd64 --variant=minbase trusty $TEMP/target http://it.archive.ubuntu.com/ubuntu/ 
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	umount $TEMP/target/boot
	umount $TEMP/target
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -e "Updating APT repos..."
apt-get -y -o RootDir=$TEMP/target update
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	umount $TEMP/target/boot
	umount $TEMP/target
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -e "Installing required packages under $TEMP/target..."
apt-get -y -o RootDir=$TEMP/target install ubuntu-minimal
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	umount $TEMP/target/boot
	umount $TEMP/target
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"





https://wiki.ubuntu.com/DebootstrapChroot










