#! /usr/bin/env python
# -*- coding:utf-8 -*-
# server.py

__author__ = 'Style'

import socket, threading, time, traceback


def tcplink(sock, addr):
    print 'Accept new connection from %s:%s' % addr
    while True:
        try:
            data = sock.recv(1024)
            time.sleep(1)
            print data
            if data == 'exit' or not data:
                break
            try:
                sock.send('You just entered command: %s' % data)
            except:
                traceback.print_exc()
                break
        except:
            traceback.print_exc()
            break
    sock.close()
    print 'Connection from %s:%s closed.' % addr


host = ''
port = 20128

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)
print 'Waiting for connection...'

while 1:
    try:
        clientsock, clientaddr = s.accept()
    except:
        traceback.print_exc()
        continue
    #创建新线程来处理TCP连接
    t = threading.Thread(target=tcplink, args=(clientsock, clientaddr))
    t.start()
    t.join()