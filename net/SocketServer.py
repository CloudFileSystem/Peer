#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket

class TCPServer:
	server_auto_bind	    = True
	server_auto_activate	= True
	allow_reuse_address 	= False
	request_queue_size  	= 256

    #---------------------------------------------------------------------------
    # For server objects operation
    #---------------------------------------------------------------------------
	def __del__(self):
		self.socket.close()

	def __init__(self, address, port):
		""" initialize address & port """
		self.server_address	= address
		self.server_port	= port

		""" create socket """
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		if self.server_auto_bind:
			self.server_bind()

		if self.server_auto_activate:
			self.server_activate()

	def server_bind(self):
		if self.allow_reuse_address:
			self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.server_address, self.server_port))
		self.server_address = self.socket.getsockname()

	def server_activate(self):
		self.socket.listen(self.request_queue_size)

	def server_close(self):
		self.socket.close()

    #---------------------------------------------------------------------------
    # For request
    #---------------------------------------------------------------------------
    def get_request(self):
        return self.socket.accept()

    def shutdown_request(self, request):
        """Called to shutdown and close an individual request."""
        try:
            #explicitly shutdown.  socket.close() merely releases
            #the socket and waits for GC to perform the actual close.
            request.shutdown(socket.SHUT_WR)
        except socket.error:
            pass #some platforms may raise ENOTCONN here
        self.close_request(request)

    def close_request(self, request):
        request.close()

if __name__ == "__main__":
	server = TCPServer('0.0.0.0', 11025)

