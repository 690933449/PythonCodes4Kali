#! /usr/bin/env python
# Basic inetd server - C3 - inetdserver.py
import sys
print 'Welcome.'
print 'Please enter a string:'
sys.stdout.flush()
line = sys.stdin.readline().strip()
print "You entered %d characters." % len(line)