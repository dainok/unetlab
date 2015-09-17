#!/bin/bash

find /opt/unetlab/data/Logs/ -type f -exec rm -f {} \;
find /opt/unetlab/data/Exports/ -type f -exec rm -f {} \;
find /var/log/ -type f -exec rm -f {} \;
find /var/cache/ -type f -exec rm -f {} \;
apt-get clean

touch /var/log/wtmp
chmod 664 /var/log/wtmp
chown root:utmp /var/log/wtmp
rm -f /etc/apt/apt.conf.d/00proxy
rm -f /opt/ovf/.configured
rm -f /etc/issue
rm -rf /root/.cache /root/.Xauthority /root/.bash_history
rm -rf /tmp/vmware-root

history -c; dd if=/dev/zero of=file bs=1M; rm -f file; poweroff
