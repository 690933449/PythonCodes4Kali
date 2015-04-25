#! /usr/bin/env python
# Information Example - C2 - connect3.py

import socket

print 'Creating socket...',
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'done.'

print 'Looking up port number...',
port = socket.getservbyname('http', 'tcp')
print 'done.'

print 'Connecting to remote host on port %d...' % port,
s.connect(('www.baidu.com', port))
print 'done.'

print 'Connected from', s.getsockname()
print 'Connected to', s.getpeername()