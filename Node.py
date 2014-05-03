#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import struct
import threading
import socket
import traceback
import hashlib

def btdebug(msg):
	""" Prints a messsage to the screen with the name of the current thread """
	print "[%s] %s" %(str(threading.currentThread().getName()),msg)

class Node:
	""" constructor for Node """
	def __init__(self, host='127.0.0.1', port=11025, debug=False):
		self.port = port
		self.host = host
		self.debug = debug
		self.shutdown = False

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

		sd = NodeConnection(sock=client_sock, debug=self.debug)
		sd.senddata('PING', 'Hello world!!')
		#client_sock.close()	

	def __debug(self, msg):
		if self.debug:
			btdebug(msg)

class NodeConnection:
	def __init__(self, host='127.0.0.1', port=11025, sock=None, debug=False):
		self.port = port
                self.host = host
                self.debug = debug

		if not sock:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((host, int(port)))
		self.sock = sock
		self.sd = self.sock.makefile('rw', 0)

	def __makemsg(self, msgtype, msgdata):
		msglen = len(msgdata)
		msg = struct.pack("!4sL%ds" %msglen, msgtype, msglen, msgdata)
		return msg

	def senddata(self, msgtype, msgdata):
		"""
		senddata( message type, message data ) -> boolean status

		Send a message through a peer connection. Returns True on success
		or False if there was an error.
		"""
		try:
			msg = self.__makemsg(msgtype, msgdata)
			self.sd.write(msg)
			self.sd.flush()
		except KeyboardInterrupt:
			raise
		except:
			if self.debug:
				traceback.print_exc()
				return False
			return True

	def recvdata(self):
		"""
		recvdata() -> (msgtype, msgdata)

		Receive a message from a peer connection. Returns (None, None)
		if there was any error.
		"""
		try:
			msgtype = self.sd.read(4)
			if not msgtype: return (None, None)

			lenstr = self.sd.read(4)
			msglen = int(struct.unpack( "!L", lenstr )[0])
			msg = ""

			while len(msg) != msglen:
				data = self.sd.read(min(2048, msglen - len(msg)))
				if not len(data):
		    			break
				msg += data

			if len(msg) != msglen:
				return (None, None)
		except KeyboardInterrupt:
			raise
		except:
			if self.debug:
				traceback.print_exc()
				return (None, None)
		return (msgtype, msg)

	def __debug(self, msg):
		if self.debug:
			btdebug(msg)

if __name__ == '__main__':
	new_node = Node(debug=True)
	new_node.start()

