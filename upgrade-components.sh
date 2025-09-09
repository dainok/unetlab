#!/bin/bash

# Alpine.js
ALPINEJS_VERSION="3.15.0"
ALPINEJS_CDN_URL="https://cdn.jsdelivr.net/npm/alpinejs@${ALPINEJS_VERSION}/dist"
wget -q -O- "${ALPINEJS_CDN_URL}/cdn.min.js" > unetlab/static/alpinejs/js/alpinejs.min.js
wget -q -O- "${ALPINEJS_CDN_URL}/cdn.min.js.map" > unetlab/static/alpinejs/js/alpinejs.min.js.map

# Cytoscape
CYTOSCAPE_VERSION="3.33.1"
CYTOSCAPE_CDN_URL="https://cdn.jsdelivr.net/npm/cytoscape@${CYTOSCAPE_VERSION}/dist"
wget -q -O- "${CYTOSCAPE_CDN_URL}/cytoscape.min.js" > unetlab/static/cytoscape/js/cytoscape.min.js
wget -q -O- "${CYTOSCAPE_CDN_URL}/cytoscape.min.js.map" > unetlab/static/cytoscape/js/cytoscape.min.js.map

# Tabler
TABLER_VERSION="1.3.2"
TABLER_CDN_URL="https://cdn.jsdelivr.net/npm/@tabler/core@${TABLER_VERSION}/dist"
wget -q -O- "${TABLER_CDN_URL}/js/tabler.min.js" > unetlab/static/tabler/js/tabler.min.js
wget -q -O- "${TABLER_CDN_URL}/js/tabler.min.js.map" > unetlab/static/tabler/js/tabler.min.js.map
wget -q -O- "${TABLER_CDN_URL}/css/tabler.min.css" > unetlab/static/tabler/css/tabler.min.css
wget -q -O- "${TABLER_CDN_URL}/css/tabler.min.css.map" > unetlab/static/tabler/css/tabler.min.css.map
