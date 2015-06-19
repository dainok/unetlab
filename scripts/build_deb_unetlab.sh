#!/bin/bash
CONTROL="/usr/src/unetlab/debian/unetlab_control.template"
SRC_DIR="/usr/src/unetlab"
ARCH=$(cat ${CONTROL} | grep Architecture | cut -d: -f2 | sed 's/ //')
BUILD_DIR="/build"
CONTROL_DIR="$(mktemp -dt)"
DATA_DIR="$(mktemp -dt)"
VERSION="$(cat ${SRC_DIR}/VERSION | cut -d- -f1)"
RELEASE="$(cat ${SRC_DIR}/VERSION | cut -d- -f2)"

cat ${CONTROL} | sed "s/%VERSION%/${VERSION}/" | sed "s/%RELEASE%/${RELEASE}/" > ${CONTROL_DIR}/control

# UNetLab
cd ${SRC_DIR}
rm -f html/includes/config.php
mkdir -p ${DATA_DIR}/opt/unetlab ${DATA_DIR}/opt/unetlab/addons ${DATA_DIR}/opt/unetlab/data/Logs ${DATA_DIR}/opt/unetlab/labs ${DATA_DIR}/opt/unetlab/tmp/ ${DATA_DIR}/opt/unetlab/scripts
rsync -a --delete html ${DATA_DIR}/opt/unetlab/
cat html/includes/init.php | sed "s/define('VERSION', .*/define('VERSION', '${VERSION}-${RELEASE}');/g" > ${DATA_DIR}/opt/unetlab/html/includes/init.php
cp -a scripts/set_uuid.php ${DATA_DIR}/opt/unetlab/scripts/
cp -a scripts/fix_iol_nvram.sh ${DATA_DIR}/opt/unetlab/scripts/
cp -a IOUtools/iou_export ${DATA_DIR}/opt/unetlab/scripts/
chown -R root:root ${DATA_DIR}/opt/unetlab
chown -R www-data:www-data ${DATA_DIR}/opt/unetlab/data ${DATA_DIR}/opt/unetlab/labs
chown -R root:unl ${DATA_DIR}/opt/unetlab/tmp
chmod 2775 -R ${DATA_DIR}/opt/unetlab/data ${DATA_DIR}/opt/unetlab/labs ${DATA_DIR}/opt/unetlab/tmp
chmod 755 ${DATA_DIR}/opt/unetlab/scripts/*

# UNetLab Wrappers and addons
cd wrappers
export CC="gcc"
export CFLAGS="-Wall -O2"
export INC="include/ts.c include/serial2udp.c include/afsocket.c include/tap.c include/cmd.c include/functions.c"
export DST="${DATA_DIR}/opt/unetlab/wrappers"
mkdir -p ${DATA_DIR}/opt/unetlab/wrappers ${DATA_DIR}/opt/unetlab/addons/iol/lib ${DATA_DIR}/opt/unetlab/addons/iol/bin ${DATA_DIR}/opt/unetlab/addons/dynamips ${DATA_DIR}/opt/unetlab/addons/qemu
${CC} ${CFLAGS} -o ${DST}/iol_wrapper ${INC} iol_wrapper.c iol_functions.c
${CC} ${CFLAGS} -o ${DST}/qemu_wrapper ${INC} qemu_wrapper.c qemu_functions.c
${CC} ${CFLAGS} -o ${DST}/dynamips_wrapper ${INC} dynamips_wrapper.c dynamips_functions.c
cp -a unl_profile ${DST}/unl_profile
cp -a unl_wrapper.php ${DST}/unl_wrapper
cd ..
cp -a /opt/unetlab/addons/iol/lib/libcrypto.so.4 ${DATA_DIR}/opt/unetlab/addons/iol/lib

# SUDO
mkdir -p ${DATA_DIR}/etc/sudoers.d
cp -a etc/sudo.conf ${DATA_DIR}/etc/sudoers.d/unetlab

# Apache
mkdir -p ${DATA_DIR}/etc/apache2/sites-available ${DATA_DIR}/etc/logrotate.d
cp -a etc/apache.conf ${DATA_DIR}/etc/apache2/sites-available/unetlab.conf
cp -a etc/logrotate.conf ${DATA_DIR}/etc/logrotate.d/unetlab

# PlyMouth
mkdir -p ${DATA_DIR}/lib/plymouth/themes/unetlab ${DATA_DIR}/etc/initramfs-tools/conf.d
rsync -a --delete plymouth/ ${DATA_DIR}/lib/plymouth/themes/unetlab/
cp -a etc/initramfs.conf ${DATA_DIR}/etc/initramfs-tools/conf.d/plymouth

# APT
mkdir -p ${DATA_DIR}/etc/apt/sources.list.d
cp -a etc/sources.list ${DATA_DIR}/etc/apt/sources.list.d/unetlab.list

# OVF Config
mkdir -p ${DATA_DIR}/etc/init ${DATA_DIR}/etc/profile.d ${DATA_DIR}/etc/init
rsync -a --delete ovf ${DATA_DIR}/opt
cp -a etc/profile.sh ${DATA_DIR}/etc/profile.d/ovf.sh
mv -f ${DATA_DIR}/opt/ovf/ovfconfig.conf ${DATA_DIR}/etc/init/ovfconfig.conf

# Post Install
cat > ${CONTROL_DIR}/postinst << EOF
#!/bin/sh
groupadd -g 32768 -f unl > /dev/null 2>&1
a2enmod rewrite > /dev/null 2>&1
a2dissite 000-default > /dev/null 2>&1
a2ensite unetlab > /dev/null 2>&1
service apache2 restart > /dev/null 2>&1
sed -i 's/.*GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash vga=788"/g' /etc/default/grub
sed -i 's/.*GRUB_GFXMODE=.*/GRUB_GFXMODE="800x600"/g' /etc/default/grub
sed -i 's/.*GRUB_HIDDEN_TIMEOUT=.*/GRUB_HIDDEN_TIMEOUT=2/g' /etc/default/grub
sed -i 's/.*GRUB_HIDDEN_TIMEOUT_QUIET=.*/GRUB_HIDDEN_TIMEOUT_QUIET=true/g' /etc/default/grub
sed -i 's/.*GRUB_TIMEOUT=.*/GRUB_TIMEOUT=0/g' /etc/default/grub
sed -i "s/^ServerName.*$/ServerName \$(hostname -f)/g" /etc/apache2/sites-available/unetlab.conf
update-alternatives --install /lib/plymouth/themes/default.plymouth default.plymouth /lib/plymouth/themes/unetlab/unetlab.plymouth 100 > /dev/null 2>&1
update-initramfs -u > /dev/null 2>&1
update-grub2 > /dev/null 2>&1
fgrep "xml.cisco.com" /etc/hosts > /dev/null || echo 127.0.0.127 xml.cisco.com >> /etc/hosts
# Fix tunctl
setcap cap_net_admin+ep /usr/sbin/tunctl > /dev/null 2>&1
setcap cap_net_admin+ep /bin/ip > /dev/null 2>&1
setcap cap_net_admin+ep /sbin/brctl > /dev/null 2>&1
setcap cap_net_admin+ep /usr/bin/ovs-vsctl > /dev/null 2>&1
# Check for Intel VT-x/AMD-V
fgrep -e vmx -e svm /proc/cpuinfo > /dev/null || echo "*** WARNING: neither Intel VT-x or AMD-V found"
# Cleaning log
rm -f /opt/unetlab/data/Logs/*
/usr/sbin/apache2ctl graceful > /dev/null 2>&1
# Mark official kernels as hold
apt-mark hold  \$(dpkg -l | grep -e linux-image -e linux-headers -e linux-generic | grep -v unetlab | awk '{print \$2}') > /dev/null 2>&1
# Setting UUID on labs
find /opt/unetlab/labs/ -name "*.unl" -exec /opt/unetlab/scripts/set_uuid.php "{}" \;
find /opt/unetlab/tmp/ -name "nvram_*" -exec /opt/unetlab/scripts/fix_iol_nvram.sh "{}" \;
EOF

# Configuring APT
cat > /etc/apt/apt.conf.d/FTPArchive.conf << EOF
APT::FTPArchive::Release::Origin "RR Labs";
APT::FTPArchive::Release::Label "RR Labs archive";
APT::FTPArchive::Release::Suite "trusty";
APT::FTPArchive::Release::Version "14.04";
APT::FTPArchive::Release::Codename "trusty";
APT::FTPArchive::Release::Architectures "amd64 i386 noarch";
APT::FTPArchive::Release::Components "rrlabs";
APT::FTPArchive::Release::Description "Route Reflector Labs";
EOF

# Building the package
cd ${DATA_DIR}
tar czf data.tar.gz *
find -type f -exec md5sum {} \; >> ${CONTROL_DIR}/md5sums
echo 2.0 > ${CONTROL_DIR}/debian-binary
cd ${CONTROL_DIR}
tar czf control.tar.gz md5sums control postinst
cd ${SRC_DIR}
mkdir -p ${BUILD_DIR}/apt/pool/trusty/u/unetlab
ar -cr ${BUILD_DIR}/apt/pool/trusty/u/unetlab/unetlab_${VERSION}-${RELEASE}_${ARCH}.deb ${CONTROL_DIR}/debian-binary ${CONTROL_DIR}/control.tar.gz ${DATA_DIR}/data.tar.gz
rm -rf ${CONTROL_DIR} ${DATA_DIR}
