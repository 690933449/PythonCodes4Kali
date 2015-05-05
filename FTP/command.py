#! /usr/bin/env python
# -*- coding:utf-8 -*-
# command.py

__author__ = 'Style'
import os, json


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
    data = {}
    with open(fullname, 'rb') as f:
        data['filename'] = fullname
        data['contents'] = f.read()
        data['length'] = len(data['contents'])
        sock.sendall(json.dumps(data))


def rec_files(sock):
    data = sock.recv(4096)
    print data

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
