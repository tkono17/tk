#!/usr/bin/python2.2
from socket import *
myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind( (myHost, myPort))
sockobj.listen(5)

while 1:
    connection, address = sockobj.accept()
    print 'Server connected by', address
    while 1:
        data = connection.recv(1024)
        if not data: break
        connection.send('Echo=>' + data)
    connection.close()
    
