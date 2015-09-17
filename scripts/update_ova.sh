#!/bin/bash

if [ $# -ne 2 ]; then
	echo "ERROR: must specify source and destination files."
	exit 1
fi

SOURCE=$1
DESTINATION=$2
TEMP=$(mktemp -d --suffix=_unetlab)
VMDK="Unified_Networking_Lab-disk1.vmdk"
QCOW="Unified_Networking_Lab-disk1.qcow2"
OVF="Unified Networking Lab.ovf"

if [ ! -f "$SOURCE" ]; then
	echo "ERROR: must specify a source OVA file."
	exit 2
fi

if [ -f "$DESTINATION" ]; then
	echo "ERROR: destination file exists."
	exit 3
fi

echo -ne "Unpacking $SOURCE to $TEMP... "
tar -C "$TEMP" -xf "$SOURCE"
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot unpack source OVA file."
	rm -rf $TEMP
	exit 4
fi
echo -e "DONE"

echo -ne "Converting $TEMP/$VMDK to $TEMP/$QCOW... "
/opt/qemu/bin/qemu-img convert -f vmdk -O qcow2 $TEMP/$VMDK $TEMP/$QCOW > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot convert VMDK to QCOW2."
	rm -rf $TEMP
	exit 5
fi
echo -e "DONE"

modprobe nbd max_part=32 > /dev/null 2>&1

echo -ne "Binding $TEMP/$QCOW on /dev/nbd0... "
/opt/qemu/bin/qemu-nbd -c /dev/nbd0 $TEMP/$QCOW > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot map QCOW2 image to /dev/nbd0."
	rm -rf $TEMP
	exit 6
fi
echo -e "DONE"

mkdir -p $TEMP/root > /dev/null 2>&1
pvscan > /dev/null 2>&1
vgchange -ay rootvg > /dev/null 2>&1

echo -ne "Mounting /dev/nbd0p1 on $TEMP/root... "
mount /dev/rootvg/rootvol $TEMP/root > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot mount root filesystem on $TEMP/root."
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 7
fi
echo -e "DONE"

echo -ne "Mounting /dev/nbd0p1 on $TEMP/root/boot... "
mount /dev/nbd0p1 $TEMP/root/boot > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot mount boot filesystem on $TEMP/root."
	umount $TEMP/root
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 8
fi
echo -e "DONE"

echo -ne "Binding /run on on $TEMP/root/run "
mount -o bind /run $TEMP/root/run > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot bind /run on $TEMP/root/run."
	umount $TEMP/root/boot
	umount $TEMP/root
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 8
fi
echo -e "DONE"

echo -ne "Running apt-get update on $TEMP/root... "
chroot $TEMP/root apt-get update > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot run apt-get update on $TEMP/root/."
	umount $TEMP/root/run
	umount $TEMP/root/boot
	umount $TEMP/root
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 9
fi
echo -e "DONE"

echo -ne "Running apt-get upgrade on $TEMP/root... "
chroot $TEMP/root apt-get -y -o Dpkg::Options::="--force-confold" upgrade > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot run apt-get upgrade on $TEMP/root/."
	umount $TEMP/root/run
	umount $TEMP/root/boot
	umount $TEMP/root
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 9
fi
echo -e "DONE"

echo -ne "Running apt-clean on $TEMP/root... "
chroot $TEMP/root apt-get clean > /dev/null 2>&1
if [ $? -ne 0 ]; then
	echo -e "FAILED"
	echo "ERROR: cannot run apt-get upgrade on $TEMP/root/."
	umount $TEMP/root/run
	umount $TEMP/root/boot
	umount $TEMP/root
	/opt/qemu/bin/qemu-nbd -d /dev/nbd0
	rm -rf $TEMP
	exit 9
fi
echo -e "DONE"

find $TEMP/root/opt/unetlab/data/Logs/ -type f -exec rm -f {} \; > /dev/null 2>&1
find $TEMP/root/opt/unetlab/data/Exports/ -type f -exec rm -f {} \; > /dev/null 2>&1
find $TEMP/root/var/log/ -type f -exec rm -f {} \; > /dev/null 2>&1
find $TEMP/root/var/cache/ -type f -exec rm -f {} \; > /dev/null 2>&1
touch $TEMP/root/var/log/wtmp > /dev/null 2>&1
chmod 664 $TEMP/root/var/log/wtmp > /dev/null 2>&1
chown root:utmp $TEMP/root/var/log/wtmp > /dev/null 2>&1
rm -f $TEMP/root/etc/apt/apt.conf.d/00proxy > /dev/null 2>&1
rm -f $TEMP/root/opt/ovf/.configured > /dev/null 2>&1
rm -f $TEMP/root/etc/issue > /dev/null 2>&1
rm -rf $TEMP/root/root/.cache $TEMP/root/root/.Xauthority $TEMP/root/root/.bash_history > /dev/null 2>&1
rm -rf $TEMP/root/tmp/vmware-root > /dev/null 2>&1

umount $TEMP/root/run
umount $TEMP/root/boot
umount $TEMP/root

echo -e "DEBUG: optimizing boot partition..."
SIZE=$(resize2fs /dev/nbd0p1 1 2>&1 | grep minimum | sed 's/^resize2fs:[^0-9]\+(\([0-9]*\))$/\1/g')
e2fsck -yf /dev/nbd0p1 > /dev/null 2>&1
resize2fs /dev/nbd0p1 $SIZE 2>&1
resize2fs /dev/nbd0p1 2>&1
mount /dev/nbd0p1 $TEMP/root
dd if=/dev/zero of=$TEMP/root/file bs=1M
rm -f $TEMP/root/file
umount $TEMP/root

echo -e "DEBUG: optimizing root partition..."
SIZE=$(resize2fs /dev/rootvg/rootvol 1 2>&1 | grep minimum | sed 's/^resize2fs:[^0-9]\+(\([0-9]*\))$/\1/g')
EXTENTS=$(($SIZE / 1024 + 1))
lvreduce -r -l $EXTENTS /dev/rootvg/rootvol
lvcreate -l 100%FREE -n freevol /dev/rootvg
dd if=/dev/zero of=/dev/rootvg/freevol bs=4M
lvremove /dev/rootvg/freevol
lvresize -r -l 100%FREE /dev/rootvg/rootvol
resize2fs /dev/rootvg/rootvol
e2fsck -yf /dev/rootvg/rootvol

cat < EOF > "Unified Networking Lab.mf"
SHA1(Unified_Networking_Lab-disk1.vmdk)= `sha1sum Unified_Networking_Lab-disk1.vmdk | cut -d' ' -f1`
EOF

tar cf $DESTINATION *ovf *vmdk *mf
