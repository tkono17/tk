#!/usr/bin/env python
#------------------------------------------------------------------
# checkmail.py
# ------------
# Check new mails on the mail server and inform me.
#------------------------------------------------------------------

import os, sys
import re
import time
import threading
import imaplib
import getpass
import datetime
import logging
import random
from Tkinter import *

log = None

class MailInfo:
    def getAddress(s):
        pass
    def __init__(self, title, fromAddress, message='', time=None):
        self.title = title
        self.fromAddress = ''
        self.toList = []
        self.ccList = []
        self.time = time
        self.message = message
        self.status = 0
    def dump(self):
        print '%s | %s | %s' % (self.title, self.fromAddress, self.message)

class Inbox:
    def __init__(self):
        self.messages = []
        pass
    def addMessage(self, m):
        self.messages.append(m)
    
class BiffPanel(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.root = None
        self.inbox = Inbox()
        self.recentMails = []
        self.recentMailsToMe = []
        self.isrunning = False 
        # self.createGui()
    def setInbox(self, inbox):
        self.inbox = inbox
    def run(self):
        if not self.isrunning:
            self.createGui()
            self.isrunning = True
        #self.update()
        #time.sleep(5)
    def update(self):
        pass
    def updateCell(self, row_col, text):
        (i, j) = row_col
        k = 3*i + j
        if k < 18:
            self.cells[k].insert(END, text)
        self.root.update()
    def createGui(self):
        # self.root = Tk()
        self.root = Tk()
        self.cells = []
        rows = []

        w0, w1, w2 = 20, 30, 50
        
        e = Entry(self.root, relief=RIDGE, width=w0)
        e.insert(END, 'From')
        e.grid(row=0, column=0, sticky=NSEW)
        self.cells.append(e)
        e = Entry(self.root, relief=RIDGE, width=w1)
        e.insert(END, 'Title')
        e.grid(row=0, column=1, sticky=NSEW)
        self.cells.append(e)
        e = Entry(self.root, relief=RIDGE, width=w2)
        e.insert(END, 'Message')
        e.grid(row=0, column=2, sticky=NSEW)
        self.cells.append(e)
        self.root.rowconfigure(0, weight=1)

        irow = 1
        for m in range(5):
            e = Entry(self.root, relief=RIDGE, width=w0)
            e.insert(END, '%s.%s' % (irow, 0))
            e.grid(row=irow, column=0, sticky=NSEW)
            self.cells.append(e)
            e = Entry(self.root, relief=RIDGE, width=w1)
            e.insert(END, '%s.%s' % (irow, 1))
            e.grid(row=irow, column=1, sticky=NSEW)
            self.cells.append(e)
            e = Entry(self.root, relief=RIDGE, width=w2)
            e.insert(END, '%s.%s' % (irow, 2))
            e.grid(row=irow, column=2, sticky=NSEW)
            self.cells.append(e)
            self.root.rowconfigure(irow, weight=1)
            irow += 1
        for icol in range(3):
            self.root.columnconfigure(icol, weight=1)

        self.root.mainloop()
##         for (irow, m) in enumerate(self.inbox.messages):
##             cols = []
##             for icol in range(0, 5):
##                 if icol==0: text = m.fromAddress
##                 elif icol==1: text = m.title
##                 elif icol==2: text = m.message
##                 #
##                 if icol==0: e = Entry(self.root, relief=RIDGE, width=20)
##                 else: e = Entry(self.root, relief=RIDGE, width=30)
##                 e.grid(row=irow, column=icol, sticky=NSEW)
##                 e.insert(END, text)
##                 self.root.rowconfigure(irow, weight=1)
##                 self.root.columnconfigure(icol, weight=1)
        pass
    
class ImapInterface:
    def connect():
        pass
    def get_header():
        pass
    def get_contents(mail):
        pass

class CheckMail(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.inbox = None
        self.imap = ImapInterface()
        self.random = random.Random()
    def connect(self):
        pass
    def get_new_mails(self):
        n = int(self.random.uniform(0, 5)) % 5
        for i in range(n):
            self.inbox.addMessage(MailInfo('message %d' % i, 'X', '-----'))
        pass
    def setInbox(self, inbox):
        self.inbox = inbox
    def dump(self):
        for m in self.inbox.messages:
            m.dump()
    def run(self):
        print 'start'
        while True:
            print 'checking ...'
            self.get_new_mails()
            self.dump()
            time.sleep(5)

class CleanMail(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.key = ''
    def run(self):
        for i in range(10000):
            print '%s cleaning ...' % self.key
            time.sleep(2)
    pass

def run():
    # start threads for each task
    log.warning('not implemented yet')
    print 'run'
    cm = CheckMail()
    cleaner = CleanMail()
    cleaner.key = 'hey'
    #cm.start()
    #cleaner.start()

def test_imap():
    # imap = imaplib.IMAP4_SSL('imap.cern.ch', 993)
    imap = imaplib.IMAP4_SSL('localhost', 2993)
    imap.login(getpass.getuser(), getpass.getpass())
    imap.select('INBOX', True) # readonly
    type, data = imap.search(None, 'UNSEEN')
    print '# returned from search'
    i = 0
    print 'n = ', len(data[0].split())
    for num in data[0].split():
        # type, data = imap.fetch(num, '(RFC822)')
        fields = '(FLAGS INTERNALDATE BODY[HEADER.FIELDS (FROM SUBJECT)])'
        type, data = imap.fetch(num, fields)
        #print 'Message %s\n%s\n' % (num, data[0][1])
        print '#------------------------'
        for x in data[:-1]:
            for y in x:
                print y
        i += 1
        # if i >= 10: break
    imap.close()
    imap.logout()
    pass
    
class Config:
    def __init__(self):
        self.enableGUI = True
        pass
    def parseArgs(self, argv):
        pass

if __name__ == '__main__':
    log = logging.getLogger('checkmail.py')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='', #filename='/tmp/myapp.log',
                        filemode='w')
    log.info('hi')
    #test_imap()
    #sys.exit(0)
    #
    log.debug('debug')
    logging.debug('hey!')
    myConfig = Config()
    myConfig.parseArgs(sys.argv)

    panel = BiffPanel()
    inbox = Inbox()
    
    #checker = CheckMail()
    #checker.setInbox(inbox)
    #checker.connect()
    #checker.start()
    
    if myConfig.enableGUI:
        print 'Create GUI'
        panel.setInbox(inbox)
        #panel.update()
        #panel.start()
    sys.exit(0)


