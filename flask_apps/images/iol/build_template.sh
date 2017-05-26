#!/bin/bash

R="\033[0;31m"
Y="\033[1;33m"
G="\033[0;32m"
U="\033[0m"

TMP="$(mktemp -dt unetlab_build_ioltemplate.XXXXXXXXXX)"
LOG="/tmp/unetlab_build_node.log"
REPOSITORY="dainok"
DOCKER="docker -H=tcp://127.0.0.1:4243"

ARCH="amd64"
SUITE="jessie"
MIRROR="http://auto.mirror.devuan.org/merged"
PACKAGES="bridge-utils curl iproute2 iptables iputils-ping net-tools procps python3 uml-utilities"

function clean {
    rm -rf ${TMP} &> /dev/null
}

trap clean EXIT
rm -f ${LOG}

dpkg -s debootstrap dchroot &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -ne "Installing dependencies... "
	apt-get -qy install debootstrap dchroot &>> ${LOG}
	if [ $? -ne 0 ]; then
		echo -e "${R}failed${U}"
		exit 1
	fi
	echo -e "${G}done${U}"
fi

export DEBIAN_FRONTEND=noninteractive
echo -ne "Building the system... "
debootstrap --variant=minbase --include=devuan-keyring --arch ${ARCH} ${SUITE} ${TMP} ${MIRROR} &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}failed${U}"
	exit 1
fi
echo -e "${G}done${U}"

cat << EOF > ${TMP}/etc/apt/sources.list
deb ${MIRROR} ${SUITE} main
deb ${MIRROR} ${SUITE}-updates main
deb ${MIRROR} ${SUITE}-security main
EOF
if [ $? -ne 0 ]; then
	echo -e "${R}Failed to set APT mirror.${U}"
	exit 1
fi

cat << EOF > ${TMP}/etc/apt/apt.conf.d/01lean
APT::Install-Suggests "0";
APT::Install-Recommends "0";
APT::AutoRemove::SuggestsImportant "false";
APT::AutoRemove::RecommendsImportant "false";
EOF
if [ $? -ne 0 ]; then
	echo -e "${R}Failed to set APT options${U}"
	exit 1
fi

echo -ne "Removing unwanted packages... "
chroot ${TMP} dpkg --purge debconf-i18n gcc-4.8-base &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}failed${U}"
	exit 1
fi
echo -e "${G}done${U}"

echo -ne "Updating APT repos... "
chroot ${TMP} apt-get update &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}failed${U}"
	exit 1
fi
echo -e "${G}done${U}"

echo -ne "Upgrading system... "
chroot ${TMP} apt-get -y dist-upgrade &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}failed${U}"
	exit 1
fi
echo -e "${G}done${U}"

# Customization for Docker
rm -f ${TMP}/usr/sbin/invoke-rc.d
ln -s /bin/true ${TMP}/usr/sbin/invoke-rc.d

echo -ne "Installing additional packages... "
chroot ${TMP} apt-get -y install ${PACKAGES} &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}failed${U}"
	exit 1
fi
echo -e "${G}done${U}"

echo -ne "Cleaning the system... "
chroot ${TMP} apt-get autoclean &>> ${LOG}
chroot ${TMP} apt-get clean &>> ${LOG}
chroot ${TMP} apt-get autoremove &>> ${LOG}
find ${TMP} -name "*-old" -exec rm -f {} \; &>> ${LOG}
rm -f ${TMP}/etc/*- ${TMP}/etc/.pwd.lock ${TMP}/var/log/*.log ${TMP}/var/lib/apt/lists/* ${TMP}/etc/ssh/ssh_host_* &>> ${LOG}
echo -e "${G}done${U}"

echo -ne "Importing system to Docker... "
tar cz -C ${TMP} . | ${DOCKER} import - dainok/nodetemplate-iol:latest &>> ${LOG}
if [ $? -ne 0 ]; then
	echo -e "${R}failed${U}"
	exit 1
fi
echo -e "${G}done${U}"

rm -rf ${LOG}
exit 0
