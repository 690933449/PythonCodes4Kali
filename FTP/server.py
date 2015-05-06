#! /usr/bin/env python
# -*- coding:utf-8 -*-
# server.py

__author__ = 'Style'

import socket, threading, traceback, os, logging, time
from command import ls, cd, send_files, rec_files

logging.basicConfig(level=logging.INFO, filename='ServerLog.txt')

def tcplink(sock, addr):
    working_dir = os.sep
    print 'Accept new connection from %s:%s' % addr
    while True:
        try:
            data = sock.recv(1024)
            logging.info('%s: Received data: %s' % (time.asctime(), data))
            data = data.strip().split(' ')
            command = data[0].lower()
            arg = data[1:]
            if command == 'ls':
                res = ls(working_dir)
                logging.info('%s: Send results: %s' % (time.asctime(), res))
                sock.send(res)
            elif command == 'director':
                sock.send(working_dir)
            elif command == 'cd':
                try:
                    working_dir = cd(working_dir, arg[0])
                    logging.info('%s: Send working director: %s' % (time.asctime(), working_dir))
                    sock.send(working_dir)
                except IOError, e:
                    logging.info('%s: cd command occurred a error: %s' % (time.asctime(), e))
                    sock.send('Error: %s' % e)
            elif command == 'get':
                filename = os.path.split(arg[0])[1]
                send_files(sock, working_dir, filename)
            elif command == 'put':
                filename = os.path.split(arg[0])[1]
                rec_files(sock, working_dir, filename)
            if command == 'exit' or not data:
                break
        except:
            traceback.print_exc()
            break
    sock.close()
    logging.info('%s: Connection from %s closed.' % (time.asctime(), addr))
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
    except KeyboardInterrupt, e:
        traceback.print_exc()
        break
    except:
        traceback.print_exc()
        continue
    #创建新线程来处理TCP连接
    t = threading.Thread(target=tcplink, args=(clientsock, clientaddr))
    t.start()
    t.join()
