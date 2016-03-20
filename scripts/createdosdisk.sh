#!/bin/bash
cd $1
pwd
cp /opt/unetlab/scripts/minidisk .
mkdir loopmnt
mount -o loop minidisk loopmnt
cp ios_config.txt loopmnt/
umount loopmnt
rm -fr loopmnt
