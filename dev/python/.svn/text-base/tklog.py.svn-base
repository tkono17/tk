#!/usr/bin/env python
#----------------------------------------------------------------------
# tklog.py
#----------------------------------------------------------------------
import os
import commands
import datetime

def log(line, out):
    dir = os.path.dirname(out)
    if not os.path.exists(dir): os.makedirs(dir)
    f = open(out, 'a')
    f.write(line + '\n')
    f.close()
    
def system(command, out):
    host = commands.getoutput('hostname')
    path = os.getcwd()
    t = datetime.datetime.now().ctime()
    s = '# Executed on %s from %s:%s' % (t, host, path)
    log(s, out)
    log(command, out)
    (status, output) = commands.getstatusoutput(command)
    log('Return status: %d' % status, out)
    return (status, output)

if __name__ == '__main__':
    system('echo hello', 'a')
    
    
