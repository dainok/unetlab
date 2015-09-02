#!/bin/bash

if [ $# -ne 1 ]; then
	echo 'ERROR: wrong options given.'
	exit 15
fi

if [ ! -f ${1} ]; then
	echo 'ERROR: file does not exist.'
	exit 15
fi

TEMP=$(mktemp -d --suffix=_unetlab)
unzip -q -o -d ${TEMP} ${1} "*.unl"
if [ $? -ne 0 ]; then
	rm -rf ${TEMP}
	echo 'ERROR: cannot unzip file.'
	exit 15
fi

find ${TEMP} -name "*.unl" -exec sed -i 's/ id="[0-9a-f-]\{36\}"//g' '{}' \;
if [ $? -ne 0 ]; then
	rm -rf ${TEMP}
	echo 'ERROR: cannot remove lab UUID.'
	exit 15
fi

cd ${TEMP}

zip -q -r -u ${1} *
if [ $? -ne 0 ]; then
	rm -rf ${TEMP}
	echo 'ERROR: cannot update files.'
	exit 15
fi

exit 0
