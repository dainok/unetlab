#!/bin/bash

FILES=$(find . -name "*.py")
for FILE in ${FILES}; do
  fgrep "__revision__" ${FILE} &> /dev/null
  if [ $? -eq 0 ]; then
    TIMESTAMP=$(date -d @$(stat --printf '%Y' ${FILE}) +%Y%m%d)
    sed -i "s/__revision__.*$/__revision__ = '${TIMESTAMP}'/g" ${FILE}
  else
    echo "Missing __revision__ on ${FILE}"
  fi
done
