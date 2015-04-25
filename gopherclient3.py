#Simple Gopher Client with file-like interface - C1
#gopherclient3.py

import socket , sys

port = 70
host = sys.argv[1]
filename = sys.argv[2]

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
except socket.gaierror as e:
    print("Error connecting to server: %s"%e)
    sys.exit(1)
fd=s.makefile('rw')

fd.write(filename + "\r\n")

for line in fd.readline():
    sys.stdout.write(line)
