#!/usr/bin/env bash

echo 'stats items'  \
	| nc localhost 11211  \
	| grep -oe ':[0-9]*:'  \
	| grep -oe '[0-9]*'  \
	| sort  \
	| uniq  \
	| xargs -L1 -I{} bash -c 'echo "stats cachedump {} 1000" | nc localhost 11211'
