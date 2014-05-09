#!/usr/bin/python
# -*- coding: utf-8 -*-
from net.request import Request
from Message import Message

if __name__ == '__main__':
	new_request = Request(debug=True)
	new_request.senddata(Message())

