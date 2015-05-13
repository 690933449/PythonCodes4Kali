#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'style'

from Tkinter import *


def hello(): print 'Hello world'
win = Tk()  # Tkinter的主窗口
win.title('Hello, Tkinter!')
win.geometry('200x100')  # Size 200, 100

btn = Button(win, text='Hello ', command=hello)
btn.pack(expand=YES, fill=BOTH)

mainloop()