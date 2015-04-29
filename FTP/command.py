#! /usr/bin/env python
# -*- coding:utf-8 -*-
# command.py

__author__ = 'Style'
import os


def ls(director):
    d = []
    for x in os.listdir(director):
        if os.path.isdir(x):
            x = x + '/'
            d.append(x)
        else:
            d.append(x)
    return d


if __name__ == "__main__":
    command = raw_input("choose a command: ")
    if command == 'ls':
        print ls('.')
    else:
        pass
