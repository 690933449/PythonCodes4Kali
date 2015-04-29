#! /usr/bin/env python
# -*- coding:utf-8 -*-
# client.py
__author__ = 'Style'

import socket, sys, pprint
from style import use_style


def create_socket(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        print 'Strange error creating socket: %s' % e
        sys.exit(1)
    print 'Connecting to server: %s:%d' % (str(ip), int(port))
    try:
        s.connect((ip, int(port)))
    except socket.gaierroe, e:
        print 'Address-related error connecting to server: %s' % e
        sys.exit(1)
    except socket.error, e:
        print 'Connection error: %s' % e
        sys.exit(1)
    return s


def send_data(sock, data):
    try:
        sock.sendall(data)
    except socket.error, e:
        print 'Error sending data: %s' % e
        sys.exit(1)


def receive_data(sock):
    try:
        buf = sock.recv(1024)
    except socket.error, e:
        print 'Error receiving data: %s' % e
        sys.exit(1)
    if not len(buf):
        return ''
    else:
        return  buf


if __name__ == '__main__':
    ip = sys.argv[1]
    port = sys.argv[2]
    s = create_socket(ip, port)
    while 1:
        data = raw_input("ftp:161220128# ")
        send_data(s, data)
        data = data.strip().split(' ')
        command = data[0]
        argus = data[1:]
        if command == 'exit':
            break
        if command == 'ls':
            while True:
                r = receive_data(s)
                print use_style(r, mode='1', fore='blue', back='green')
        else:
            print 'Failed!'
            break
    s.close()
