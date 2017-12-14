#!/usr/bin/env python

import imaplib
import socket
import string
import sys

class SSLFile:
	def __init__(self, sock):
		self.sock = sock
		self.client = socket.ssl(sock, None, None)
		self.buffer = ''
		self.eof = 0
	def send(self, t, x=0):
		return self.client.write(t)
	def read(self, n):
		if self.buffer:
			r = self.buffer[:n]
			self.buffer = self.buffer[n:]
			n -= len(r)
		else:
			r = ''
		if self.eof:
			return r
		while n > 0:
			c = self.client.read(n)
			if not c:
				self.eof = 1
				break
			if len(c) <= n:
				f = c
			else:
				f = c[:n]
				self.buffer += c[n:]
			n -= len(f)
			r += f
		return r
	def write(self, t):
		return self.client.write(t)
	def readline(self):
		while 1:
			rl = self.buffer.split('\n', 1)
			if len(rl) > 1:
				self.buffer = rl[1]
				return rl[0] + '\n'
			if self.eof:
				r = self.buffer
				self.buffer = ''
				return r
			c = self.client.read()
			if not c:
				self.eof = 1
			else:
				self.buffer += c

class IMAP4(imaplib.IMAP4):
	def open(self, host, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))
		self.sock = SSLFile(sock)
		self.file = self.sock

if len(sys.argv) > 2:
	p = string.atoi(sys.argv[2])
else:
	p = 993
i = IMAP4(sys.argv[1], p)
print i.capabilities
