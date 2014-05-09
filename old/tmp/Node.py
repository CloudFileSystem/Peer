#!/usr/bin/python
# -*- coding: utf-8 -*-
from net.server import Server
from Message import Message

app = Server(debug=True)
@app.addCallback(Message)
def read():
	print "read"

if __name__ == '__main__':
	app.start()

