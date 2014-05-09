#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import inspect
import threading

from request import Request
from debug import btdebug

class Server:
	def __init__(self, host='127.0.0.1', port=11025, debug=False):
		self.port = port
		self.host = host
		self.debug = debug
		self.shutdown = False
		self.callback = dict()

	def __getServerSocket(self, port, backlog=10):
		"""
		Constructs and prepares a server socket listening
		on the given port.
		"""
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(('', port))
		sock.listen(backlog)
		return sock

	"""
	waiting for user access
	"""
	def start(self, defaulttimeout=None):
		server_sock = self.__getServerSocket(self.port)
		server_sock.settimeout(defaulttimeout)
		self.__debug( 'Server started: (%s:%d)' %(self.host, self.port))

		while not self.shutdown:
			try:
				self.__debug('Listening for connections...')
				client_sock, client_addr = server_sock.accept()
				client_sock.settimeout(None)

				thread = threading.Thread(
					target = self.__handle_peer,
					args = [client_sock])
				
				thread.start()
			except KeyboardInterrupt:
				print 'KeyboardInterrupt: stopping mainloop'
				self.shutdown = True
				continue
			except socket.timeout:
				pass
			except:
				if self.debug:
					traceback.print_exc()
					continue

		# end while loop
		self.__debug('Main loop exiting')
		server_sock.close()

	def __handle_peer(self, client_sock):
		"""
		handlepeer( new socket connection ) -> ()
		Dispatches messages from the socket connection
		"""
		self.__debug('New child ' + str(threading.currentThread().getName()))
		self.__debug('Connected ' + str(client_sock.getpeername()))

		sd = Request(sock=client_sock, debug=self.debug)
		try:
			while not self.shutdown:
				message = sd.recvdata()
				if self.callback.has_key(message.__class__.__name__):
					self.callback[message.__class__.__name__]()
		except EOFError:
			self.__debug('EOFError...')
		client_sock.close()

	def addCallback(self, message):
		def new(method):
			if not self.callback.has_key(method):
				self.callback[message.__name__] = method
		return new	

	def __debug(self, msg):
		if self.debug:
			btdebug(msg)

if __name__ == '__main__':
	Server(debug=True).start()

