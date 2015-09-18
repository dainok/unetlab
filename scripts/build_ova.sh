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

export DEBIAN_FRONTEND="noninteractive"

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
chroot $TEMP/target apt-get -o Dpkg::Options::="--force-confold" --force-yes -fuy install ubuntu-minimal apparmor cron curl dmsetup grub-common grub-pc init-system-helpers kbd keyboard-configuration lvm2 mime-support nano ncurses-term openssh-server openssh-sftp-server pciutils sharutils telnet ucf vlan xkb-data 
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	umount $TEMP/target/boot
	umount $TEMP/target
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

echo -ne "Installing RR Labs key under $TEMP/target..."
curl -s http://www.unetlab.com/rrlabs.key | chroot $TEMP/target apt-key add - > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	umount $TEMP/target/boot
	umount $TEMP/target
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 1
fi
echo -e "DONE"

cat > $TEMP/target/etc/apt/sources.list << EOF
# See http://help.ubuntu.com/community/UpgradeNotes for how to upgrade to
# newer versions of the distribution.
deb http://us.archive.ubuntu.com/ubuntu/ trusty main restricted
deb-src http://us.archive.ubuntu.com/ubuntu/ trusty main restricted

## Major bug fix updates produced after the final release of the
## distribution.
deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates main restricted
deb-src http://us.archive.ubuntu.com/ubuntu/ trusty-updates main restricted

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team. Also, please note that software in universe WILL NOT receive any
## review or updates from the Ubuntu security team.
deb http://us.archive.ubuntu.com/ubuntu/ trusty universe
deb-src http://us.archive.ubuntu.com/ubuntu/ trusty universe
deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates universe
deb-src http://us.archive.ubuntu.com/ubuntu/ trusty-updates universe

deb http://security.ubuntu.com/ubuntu trusty-security main
deb-src http://security.ubuntu.com/ubuntu trusty-security main
deb http://security.ubuntu.com/ubuntu trusty-security universe
deb-src http://security.ubuntu.com/ubuntu trusty-security universe
deb http://security.ubuntu.com/ubuntu trusty-security multiverse
deb-src http://security.ubuntu.com/ubuntu trusty-security multiverse

## Uncomment the following two lines to add software from Canonical's
## 'partner' repository.
## This software is not part of Ubuntu, but is offered by Canonical and the
## respective vendors as a service to Ubuntu users.
# deb http://archive.canonical.com/ubuntu trusty partner
# deb-src http://archive.canonical.com/ubuntu trusty partner

## Uncomment the following two lines to add software from Ubuntu's
## 'extras' repository.
## This software is not part of Ubuntu, but is offered by third-party
## developers who want to ship their latest software.
# deb http://extras.ubuntu.com/ubuntu trusty main
# deb-src http://extras.ubuntu.com/ubuntu trusty main
EOF

cat > $TEMP/target/etc/apt/sources.list.d/unetlab.list << EOF
deb http://public.routereflector.com/apt trusty rrlabs
EOF

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

echo -e "Installing UNetLab under $TEMP/target..."
chroot $TEMP/target apt-get -o Dpkg::Options::="--force-confold" --force-yes -fuy install unetlab
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










