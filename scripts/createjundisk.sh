#!/bin/bash
cd $1
dd if=/dev/zero of=minidisk bs=1M count=64
echo -e 'n\np\n1\n\n\nt\nb\nw\n\n' | fdisk  minidisk
modprobe nbd
for i in $(seq 0 15)
        do /opt/qemu/bin/qemu-nbd -f raw -c /dev/nbd${i} minidisk  && break
done
mkdosfs /dev/nbd${i}p1
mkdir disk
mount /dev/nbd${i}p1 disk
cp startup-config disk/startup-config
umount disk
/opt/qemu/bin/qemu-nbd -d /dev/nbd${i}
rm -fr disk
