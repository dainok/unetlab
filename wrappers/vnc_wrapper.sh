#!/bin/bash
IP=$(echo $1 | sed 's/vnc:\/\/\([0-9.]*\):\([0-9]*\)/\1/g')
PORT=$(echo $1 | sed 's/vnc:\/\/\([0-9.]*\):\([0-9]*\)/\2/g')
/usr/bin/xtightvncviewer $IP::$PORT
