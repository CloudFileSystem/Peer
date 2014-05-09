#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import struct
from message import AbstractMessage

DEFAULT_TCPSERVER_PORT=11025
MAX_DATA_SIZE=1500

class TCPClient(object):
	def __init__(self, host, port=DEFAULT_TCPSERVER_PORT):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                #sock.settimeout(self.timeout)

		try:
			self.sock.connect((host, port))
			data = 'Hello world!!'
			self.sock.send(AbstractMessage(0).encode('Hello Naoya'))
		except (socket.error, socket.timeout):
			print 'error request'

if __name__ == '__main__':
	client = TCPClient('127.0.0.1')
