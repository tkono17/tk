#!/usr/bin/env python
import getpass, imaplib
import sys

user_name = r'PHYSICS\kohno\t.kohno1'

M = imaplib.IMAP4_SSL('exchng3.physics.ox.ac.uk')
# print M.getquota()

print user_name
M.login(user_name, getpass.getpass())
M.select()
i = 0
n = 2
typ, data = M.search(None, 'ALL')
for num in data[0].split():
    type, data = M.fetch(num, '(RFC822)')
    # print 'Message %s\n%s\n' % (num, data[0][1])
    if i==n:
        print 'Message %s\n' % (num) # message number in that folder
        print 'len data = ', len(data)
        print 'len data[0] = ', len(data[0])
        print 'data 0 = ', data[0] # message
        print 'data 0-0 = ', data[0][0] # message header
        print 'data 0-1 = ', data[0][1] # message content
        print 'data 1 = ', data[1]
    if i>n: break
    i += 1
M.logout()
