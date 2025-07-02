#!/bin/bash
VERSION="1.3.2"
BASE_URL="https://cdn.jsdelivr.net/npm/@tabler/core@${VERSION}/dist"

set -e
rm -rf unetlab/static/tabler
mkdir -p unetlab/static/tabler/css unetlab/static/tabler/js

wget -q -O- "${BASE_URL}/js/tabler.min.js" > unetlab/static/tabler/js/tabler.min.js
wget -q -O- "${BASE_URL}/css/tabler.min.css" > unetlab/static/tabler/css/tabler.min.css
wget -q -O- "${BASE_URL}/css/tabler-flags.min.css" > unetlab/static/tabler/css/tabler-flags.min.css
wget -q -O- "${BASE_URL}/css/tabler-payments.min.css" > unetlab/static/tabler/css/tabler-payments.min.css
wget -q -O- "${BASE_URL}/css/tabler-social.min.css" > unetlab/static/tabler/css/tabler-social.min.css
wget -q -O- "${BASE_URL}/css/tabler-vendors.min.css" > unetlab/static/tabler/css/tabler-vendors.min.css
