#! /usr/bin/env python
# Get list of available socket options -- C3 -- sockopts.py

import socket
solist = [x for x in dir(socket) if x.startswith('SO_')]
solist.sort()
for x in solist:
	print x