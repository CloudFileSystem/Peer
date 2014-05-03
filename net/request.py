#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import socket
from debug import btdebug

class Request:
	def __init__(self, host='127.0.0.1', port=11025, sock=None, debug=False):
		self.port = port
		self.host = host
		self.debug = debug

		if not sock:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((host, int(port)))
		self.sock = sock
		self.sd = self.sock.makefile('rw', 0)

	def senddata(self, data):
		pickle.dump(data, self.sd)

	def recvdata(self):
		return pickle.load(self.sd)

	def __debug(self, msg):
		if self.debug:
			btdebug(msg)

