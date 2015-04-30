#!/bin/bash

# Fixing setcap
setcap cap_net_admin+ep /usr/sbin/tunctl
setcap cap_net_admin+ep /bin/ip
setcap cap_net_admin+ep /sbin/brctl
setcap cap_net_admin+ep /usr/bin/ovs-vsctl

# Deleting logs
rm -f /opt/unetlab/data/Logs/*
/usr/sbin/apache2ctl graceful

# Setting /etc/issue
echo "Unified Networking Lab (default root password is 'unl')" > /etc/issue
if [[ -e "/sys/class/net/pnet0" ]]; then
    INTERFACE="pnet0"
    IP="$(ifconfig ${INTERFACE} 2> /dev/null | grep 'inet addr' | cut -d: -f2 | cut -d' ' -f1 | grep -E "^[0-9]+.[0-9]+.[0-9]+.[0-9]+$")"
    if [[ $? -eq 0 ]]; then
        echo "Use http://${IP}/" >> /etc/issue
    else
        echo "No IP address on interface ${INTERFACE}" >> /etc/issue
    fi
elif [[ -e "/sys/class/net/eth0" ]]; then
    INTERFACE="eth0"
    IP="$(ifconfig ${INTERFACE} 2> /dev/null | grep 'inet addr' | cut -d: -f2 | cut -d' ' -f1 | grep -E "^[0-9]+.[0-9]+.[0-9]+.[0-9]+$")"
    if [[ $? -eq 0 ]]; then
        echo "Use http://${IP}/" >> /etc/issue
    else
        echo "No IP address on interface ${INTERFACE}" >> /etc/issue
    fi
else
    INTERFACE=""
    IP=""
    echo "No suitable interface found" >> /etc/issue
fi
fgrep -e vmx -e svm /proc/cpuinfo 2>&1 > /dev/null
if [[ $? -eq 0 ]]; then
cat >> /etc/issue << EOF

EOF
else
cat >> /etc/issue << EOF

WARNING: neither Intel VT-x or AMD-V found

EOF
fi
