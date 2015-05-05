#! /usr/bin/env python
# -*- coding:utf-8 -*-
# client.py
__author__ = 'Style'

import socket, sys, json, logging, time, os
from style import use_style
from command import cd, ls, rec_files

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
    except socket.gaierror, e:
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


def handle_client(com, lo_dir):
    com = com.strip().split(' ')
    command = com[0]
    argus = com[1:]
    if command == 'dir':
        for x in handle_json(ls(lo_dir)):
            print x
        return ''
    elif command == 'lcd':
        lo_dir = cd(lo_dir, argus[0])
        return lo_dir
    else:
        print 'error!'
        return ''



if __name__ == '__main__':
    ip = sys.argv[1]
    port = sys.argv[2]
    s = create_socket(ip, port)
    re_working_dir = get_working_dir(s)
    lo_working_dir = os.sep
    while 1:
        data = raw_input("ftp@161220128:local:%s to remote:%s#" % (lo_working_dir, re_working_dir))
        if 'dir' in data or 'lcd' in data:
            res = handle_client(data, lo_working_dir)
            if len(res):
                lo_working_dir = res
            else:
                pass
        else:
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
            elif command == 'put':
                pass
            elif command == 'get':
                rec_files(s)
            else:
                print 'Wrong command!(you should input command:ls, cd, put, get, dir, lcd)'
    s.close()
