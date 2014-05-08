#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from message import AbstractMessage

DEFAULT_TCPSERVER_PORT=11025
MAX_DATA_SIZE=1500

class TCPServer(object):
	def __init__(self, host='0.0.0.0', port=DEFAULT_TCPSERVER_PORT, timeout=0):
		# server state
		self.active = False

		# connections
		self.connections = dict()

		# create and bind socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((host, port))

		self.sock.listen(256)

	def _work(self):
		try:
			while self.active:
				sock, _ = self.sock.accept()
				try:
					#sock2.settimeout(0.5)
					addrinfo = sock.getpeername()

					data = sock.recv(MAX_DATA_SIZE)
					#print AbstractMessage(0).decode(str(data))
					print data, addrinfo
				except (socket.error, socket.timeout):
					print 'timeout'
					sock.close()
					continue
				finally:	
					sock.close()
		except KeyboardInterrupt:
			self.sock.close()

	def start(self):
		self.active = True
		self._work()

if __name__ == '__main__':
	server = TCPServer(host='127.0.0.1')
	server.start()

