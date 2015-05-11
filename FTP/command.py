#! /usr/bin/env python
# -*- coding:utf-8 -*-
# command.py

__author__ = 'Style'
import os, json, logging, struct

logging.basicConfig(level=logging.INFO, filename='CommandLog.txt')


def ls(director):
    l = []
    for x in os.listdir(director):
        x = os.path.join(director, x)
        if os.path.isdir(x):
            x = x + os.sep
            l.append(x)
        else:
            l.append(x)
    d = {}
    for i in range(len(l)):
        d[i] = l[i]
    return json.dumps(d)


def cd(working_dir, director):
    if director == '.':
        pass
    elif director == '..':
        working_dir = os.path.split(working_dir)[0]
    elif director[0] == os.sep:
        if os.path.isdir(director):
            working_dir = director
        else:
            raise IOError('No such file or director')
    else:
        d = os.path.join(working_dir, director)
        if not os.path.isdir(d):
            raise  IOError('No such file or director')
        else:
            working_dir = d
    return  working_dir


def send_files(sock, director, filename):
    fullname = os.path.join(director, filename)
    if not os.path.isfile(fullname):
        sock.send('er')
    else:
        sock.send('ok')
        with open(fullname, 'rb') as f:
            data = f.read()
            sock.send('%16d' % os.path.getsize(fullname))
            sock.sendall(data)


def rec_files(sock, working_dir,filename):
    res = sock.recv(2)
    if res == 'er':
        print 'No such file or wrong director'
    elif res == 'ok':
        FILE_SIZE =int(sock.recv(16))
        logging.info('get the file size: %s' % FILE_SIZE)
        data = ''
        while len(data) < FILE_SIZE:
            data += sock.recv(8)
        file_dir = os.path.join(working_dir, filename)
        if os.path.isfile(file_dir):
            file_dir = os.path.join(working_dir, 'new_' + filename)
        print 'Receiving file: %s' % filename
        with open(file_dir,'wb') as f:
            f.write(data)
    else:
        print 'Failed to receive files.'

if __name__ == "__main__":
    working_dir = os.sep
    while True:
        data = raw_input("choose a command: ")
        data = data.strip().split(' ')
        command = data[0]
        arg = data[1:]
        if command == 'exit':
            break
        elif command == 'ls':
            print ls(working_dir)
        elif command == 'cd':
            try:
                working_dir = cd(working_dir, arg[0])
                print working_dir
            except IOError, e:
                print e
                continue
        else:
            pass
