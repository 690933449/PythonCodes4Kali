#!/usr/bin/env python
# Server With Error Handling - C3 - errorserver.py
import socket, traceback

host = ''
port = 51423

s = socket.socket(socket.AF_INET, socket.STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)

while 1:
	try:
		clientsock, clientaddr = s.accept()
	except:
		traceback.print_exc()
		continue

#Process the connections

	try:
		print "Got connections from", clientsock.getpeername()
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		tracebak.print_exc()

#Close the connection

	try:
		clientsock.close()
	except KeyboardInterrupt:
		raise
	except:
		tracback.print_exc()