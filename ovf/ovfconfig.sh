#!/bin/bash

# Check if VM is alredy configured
if [[ -e /opt/ovf/.configured ]]; then
    exit
fi

. ~/.profile

TITLE="Unified Networking Lab - Setup"

# Checking if eth0 exists
if [[ ! -e "/sys/class/net/eth0" ]]; then
    dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Networking' --msgbox '\nInterface eth0 not found.' 7 40
    exit
fi

# Setting root password
ovf_root_password='uninitialized'
while [[ ${ovf_root_password} != ${ovf_root_repeat_password} ]]; do
	ovf_root_password=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Root Password' --passwordbox 'Type the Root Password:' 8 40 '')
	ovf_root_repeat_password=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Root Password' --passwordbox 'Repeat the Root Password:' 8 40 '')
	if [[ ${ovf_root_password} != ${ovf_root_repeat_password} ]]; then
		dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Root Password' --msgbox '\nPasswords do not match.' 7 40
	else
		echo root:"${ovf_root_password}" | chpasswd 2>&1 > /dev/null
        if [ $? -ne 0 ]; then
            dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Root Password' --msgbox '\nFailed to change password.' 7 40
        fi
	fi
done

# Checking if ovf parameters exist
vmtoolsd --cmd "info-get guestinfo.ovfEnv" 2> /dev/null > /opt/ovf/ovf.xml

if [ $? -eq 0 ]; then
	# Using ovf parameters from ESXi
	xsltproc /opt/ovf/ovf.xsl /opt/ovf/ovf.xml | sed 's/vami\.//' | sed 's/\.unetlab//' > /opt/ovf/ovf_vars
	. /opt/ovf/ovf_vars
else
	# Using interactive input
	ovf_hostname=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Hostname' --inputbox 'Type the short hostname for the system:' 9 40 'unl01')
	ovf_domain=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'DNS domain name' --inputbox 'Type the DNS domain name for the system:' 9 40 'example.com')
	ovf_dhcp=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Use DHCP/Static IP Address' --radiolist 'Use DHCP or Static IP Address for the network adapter on Management Network?' 11 40 2 'dhcp' '' 'on' 'static' '' 'off')

	if [[ "${ovf_dhcp}" = 'static' ]]; then
		# If DHCP is not used, ask for IP address/netmask/gateway/dns
		ovf_ip=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Management Network IP Address' --inputbox 'Type the IP address for the Management Network:' 9 40 '')
		ovf_netmask=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Management Network Subnet Mask' --inputbox 'Type the Subnet Mask for the Management Network:' 9 40 '')
		ovf_gateway=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Management Network Default Gateway' --inputbox 'Type the Default Gateway for the Management Network:' 9 40 '')
		ovf_dns1=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Primary DNS server' --inputbox 'Type the IP IP address of primary DNS server:' 9 40 '')
		ovf_dns2=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Secondary DNS server' --inputbox 'Type the IP address of secondary DNS server:' 9 40 '')
	fi

	ovf_ntp=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'NTP server' --inputbox 'Type the hostname/IP address of NTP for initial clock sync (leave empty if not used):' 10 40 '')

	ovf_proxy_type=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Proxy Server configuration' --radiolist 'Choose how the VM can connect to the Internet.' 11 40 3 'direct connection' '' 'on' 'anonymous proxy' '' 'off' 'authenticated proxy' '' 'off')
	if [[ ${ovf_proxy_type} = 'anonymous proxy' || ${ovf_proxy_type} = 'authenticated proxy' ]]; then
		ovf_proxy_url=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Proxy Server and port' --inputbox 'Type the Proxy Server URL:' 8 40 'proxy.example.com:8080')
	fi
	if [[ ${ovf_proxy_type} = 'authenticated proxy' ]]; then
		ovf_proxy_username=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Proxy Server Username' --inputbox 'Type the Proxy Server Username:' 8 40 '')
		ovf_proxy_password='uninitialized'
		while [[ ${ovf_proxy_password} != ${ovf_proxy_repeat_password} ]]; do
			ovf_proxy_password=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Proxy Server Password' --passwordbox 'Type the Proxy Server Password:' 8 40 '')
			ovf_proxy_repeat_password=$(dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Proxy Server Password' --passwordbox 'Repeat the Proxy Server Password:' 8 40 '')
			if [[ ${ovf_proxy_password} != ${ovf_proxy_repeat_password} ]]; then
				dialog --backtitle "${TITLE}" --no-cancel --stdout --title 'Proxy Server Password' --msgbox '\nPasswords do not match.' 7 40
			fi
		done
	fi
fi

# Setting Hostname and Domain Name
echo ${ovf_hostname} > /etc/hostname
sed -i "s/127.0.1.1.*/127.0.1.1\t${ovf_hostname}.${ovf_domain}\t${ovf_hostname}/g" /etc/hosts

# Setting Management Network
cat > /etc/network/interfaces << EOF
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
iface eth0 inet manual
auto pnet0
EOF

if [[ "${ovf_dhcp}" = 'static' ]]; then
    echo "iface pnet0 inet static" >> /etc/network/interfaces
    echo "    address ${ovf_ip}" >> /etc/network/interfaces
    echo "    netmask ${ovf_netmask}" >> /etc/network/interfaces
    echo "    gateway ${ovf_gateway}" >> /etc/network/interfaces
    echo "    dns-domain ${ovf_domain}" >> /etc/network/interfaces
    echo "    dns-nameservers ${ovf_dns1} ${ovf_dns2}" >> /etc/network/interfaces
    echo "    bridge_ports eth0" >> /etc/network/interfaces
    echo "    bridge_stp off" >> /etc/network/interfaces
else
    echo "iface pnet0 inet dhcp" >> /etc/network/interfaces
    echo "    bridge_ports eth0" >> /etc/network/interfaces
    echo "    bridge_stp off" >> /etc/network/interfaces
fi

cat >> /etc/network/interfaces << EOF

# Cloud devices
iface eth1 inet manual
auto pnet1
iface pnet1 inet manual
    bridge_ports eth1
    bridge_stp off

iface eth2 inet manual
auto pnet2
iface pnet2 inet manual
    bridge_ports eth2
    bridge_stp off

iface eth3 inet manual
auto pnet3
iface pnet3 inet manual
    bridge_ports eth3
    bridge_stp off

iface eth4 inet manual
auto pnet4
iface pnet4 inet manual
    bridge_ports eth4
    bridge_stp off

iface eth5 inet manual
auto pnet5
iface pnet5 inet manual
    bridge_ports eth5
    bridge_stp off

iface eth6 inet manual
auto pnet6
iface pnet6 inet manual
    bridge_ports eth6
    bridge_stp off

iface eth7 inet manual
auto pnet7
iface pnet7 inet manual
    bridge_ports eth7
    bridge_stp off

iface eth8 inet manual
auto pnet8
iface pnet8 inet manual
    bridge_ports eth8
    bridge_stp off

iface eth9 inet manual
auto pnet9
iface pnet9 inet manual
    bridge_ports eth9
    bridge_stp off
EOF

# Setting the NTP server
if [ "${ovf_ntp}" != '' ]; then
    sed -i 's/NTPDATE_USE_NTP_CONF=.*/NTPDATE_USE_NTP_CONF=no/g' /etc/default/ntpdate
    sed -i 's/NTPSERVERS=.*/NTPSERVERS=${ovf_ntp}/g' /etc/default/ntpdate
else
    sed -i 's/NTPDATE_USE_NTP_CONF=.*/NTPDATE_USE_NTP_CONF=yes/g' /etc/default/ntpdate
    sed -i 's/NTPSERVERS=.*/NTPSERVERS=/g' /etc/default/ntpdate
fi

# Setting the proxy server
if [ "${ovf_proxy_type}" = "direct connection" ]; then
    rm -f /etc/apt/apt.conf.d/00proxy
elif [ "${ovf_proxy_type}" = "anonymous proxy" ]; then
    echo Acquire::http::Proxy "http://${ovf_proxy_url}/" > /etc/apt/apt.conf.d/00proxy
    echo Acquire::https::Proxy "http://${ovf_proxy_url}/" >> /etc/apt/apt.conf.d/00proxy
    echo Acquire::ftp::Proxy "http://${ovf_proxy_url}/" >> /etc/apt/apt.conf.d/00proxy
elif [ "${ovf_proxy_type}" = "authenticated proxy" ]; then
    echo "Acquire::http::Proxy \"http://${ovf_proxy_username}:${ovf_proxy_password}@${ovf_proxy_url}/\";" > /etc/apt/apt.conf.d/00proxy
    echo "Acquire::https::Proxy \"http://${ovf_proxy_username}:${ovf_proxy_password}@${ovf_proxy_url}/\";" >> /etc/apt/apt.conf.d/00proxy
    echo "Acquire::ftp::Proxy \"http://${ovf_proxy_username}:${ovf_proxy_password}@${ovf_proxy_url}/\";" >> /etc/apt/apt.conf.d/00proxy
fi

# Cleaning
rm -rf /etc/ssh/ssh_host_* /root/.Xauthority /root/.ssh /root/.bash_history /tmp/ssh* /opt/unetlab/tmp/* /tmp/netio* /tmp/vmware* /opt/ovf/ovf_vars /opt/ovf/ovf.xml /root/.bash_history /root/.cache
find /var/log -type f -exec rm -f {} \;
find /var/lib/apt/lists -type f -exec rm -f {} \;
find /opt/unetlab/data/Logs -type f -exec rm -f {} \;
touch /var/log/wtmp
chown root:utmp /var/log/wtmp
chmod 664 /var/log/wtmp
apt-get clean
dpkg-reconfigure openssh-server

# Ending and rebooting
touch /opt/ovf/.configured
reboot
