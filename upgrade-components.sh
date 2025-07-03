#!/bin/bash

# Tabler
VERSION="1.3.2"
CDN_URL="https://cdn.jsdelivr.net/npm/@tabler/core@${VERSION}/dist"

wget -q -O- "${CDN_URL}/js/tabler.min.js" > unetlab/static/tabler/js/tabler.min.js
wget -q -O- "${CDN_URL}/css/tabler.min.css" > unetlab/static/tabler/css/tabler.min.css
