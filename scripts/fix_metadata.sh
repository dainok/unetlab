#!/bin/bash
# vim: syntax=sh tabstop=4 softtabstop=0 noexpandtab laststatus=1 ruler

FILES=$(fgrep -Rl "@author Andrea Dainese" html wrappers scripts)

AUTHOR="Andrea Dainese \<andrea.dainese@gmail.com\>"
COPYRIGHT="2014-2016 Andrea Dainese"
LICENSE="BSD-3-Clause https:\/\/github.com\/dainok\/unetlab\/blob\/master\/LICENSE"
LINK="http:\/\/www.unetlab.com\/"

#TODO  exiftool -owner='Andrea Dainese <andrea.dainese@gmail.com>' -copyright='Andrea Dainese <andrea.dainese@gmail.com>' -author='Eugenia Paffile <eugenia.paffile@gmail.com>' -comment='Part of UNetLab software (http://www.unetlab.com/)' *


for f in ${FILES}; do
	if [ "${f}" = "scripts/fix_metadata.sh" ]; then
		continue
	fi
    VERSION=$(date -d @$(stat --printf '%Y' ${f}) +%Y%m%d)
	TIMESTAMP=$(date -d @$(stat --printf '%Y' ${f}) +%Y%m%d%H%M)
	sed -i "s/@author .*$/@author ${AUTHOR}/g" ${f}
	sed -i "s/@copyright .*$/@copyright ${COPYRIGHT}/g" ${f}
	sed -i "s/@license .*$/@license ${LICENSE}/g" ${f}
	sed -i "s/@link .*$/@link ${LINK}/g" ${f}
	sed -i "s/@version .*$/@version ${VERSION}/g" ${f}
	fgrep "# ${f}" ${f} > /dev/null 2>&1 || fgrep "* ${f}" ${f} > /dev/null 2>&1
	if [ $? -ne 0 ]; then
		echo "Missing or wrong file on header (${f})"
	fi
	dos2unix ${f} > /dev/null 2>&1
	touch -t ${TIMESTAMP} ${f}
done
