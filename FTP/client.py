#! /usr/bin/env python
# -*- coding:utf-8 -*-
# client.py
__author__ = 'Style'

import socket, sys, json, logging, time, os
from style import use_style

logging.basicConfig(level=logging.INFO, filename='log.txt')

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
        buf = sock.recv(4096)
    except socket.error, e:
        print 'Error receiving data: %s' % e
        sys.exit(1)
    if not len(buf):
        return ''
    else:
        return  buf


def get_working_dir(s):
    send_data(s,'director')
    r = receive_data(s)
    return r

def handle_json(json_str):
    logging.info('%s: json_str: %s' % (time.asctime(), json_str))
    d = json.loads(json_str)
    return list(d.itervalues())




if __name__ == '__main__':
    ip = sys.argv[1]
    port = sys.argv[2]
    s = create_socket(ip, port)
    re_working_dir = get_working_dir(s)
    lo_working_dir = os.sep
    while 1:
        data = raw_input("ftp@161220128:%s#" % re_working_dir)
        send_data(s, data)
        data = data.strip().split(' ')
        command = data[0]
        argus = data[1:]
        if command == 'exit':
            break
        if command == 'ls':
            r = receive_data(s)
            if len(r):
                for x in handle_json(r):
                    print x
            else:
                break
        elif command == 'cd':
            r = receive_data(s)
            if not 'Error' in r:
                re_working_dir = r
            else:
                print r
        else:
            print 'Failed!'
            break
    s.close()
