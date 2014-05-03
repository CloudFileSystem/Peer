#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading

def btdebug(msg):
	"""
	Prints a messsage to the screen with the name
	of the current thread
	"""
	print "[%s] %s" %(str(threading.currentThread().getName()),msg)

if __name__ == '__main__':
	btdebug('Hello world!!')

