#!/bin/bash

FILES=$(find . -name "*.py")
for FILE in ${FILES}; do
  fgrep "__revision__" ${FILE} &> /dev/null
  if [ $? -eq 0 ]; then
    TIMESTAMP=$(date -d @$(stat --printf '%Y' ${FILE}) +%Y%m%d)
    fgrep "__revision__ = '${TIMESTAMP}'" ${FILE} &> /dev/null
    if [ $? -eq 0 ]; then
      sed -i "s/__revision__.*$/__revision__ = '${TIMESTAMP}'/g" ${FILE}
    fi
  else
    echo "Missing '__revision__' on ${FILE}"
  fi
done

FILES=$(find . -name "*.dockerfile")
for FILE in ${FILES}; do
  fgrep "LABEL version" ${FILE} &> /dev/null
  if [ $? -eq 0 ]; then
    TIMESTAMP=$(date -d @$(stat --printf '%Y' ${FILE}) +%Y%m%d)
    fgrep "LABEL version = '${TIMESTAMP}'" ${FILE} &> /dev/null
    if [ $? -eq 0 ]; then
      sed -i "s/LABEL version.*$/LABEL version = '${TIMESTAMP}'/g" ${FILE}
    fi
  else
    echo "Missing 'LABEL version' on ${FILE}"
  fi
done
