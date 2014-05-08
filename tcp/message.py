#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
from abc import ABCMeta, abstractmethod

class AbstractMessage(object):
	__metaclass__ = ABCMeta

	def __init__(self, ptype):
		self.ptype	= ptype

	def encode(self, message):
		return struct.pack('ii1000s', self.ptype, len(message), message)

	def decode(self, data):
		return struct.unpack('ii1000s', str(data))

if __name__ == '__main__':
	message = AbstractMessage(1)
	data = message.encode('Hello world!!')
	print message.decode(data)
	#pass

