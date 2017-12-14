#!/usr/bin/env python

import os
import re
import subprocess

def listDatasets(pattern):
    cmd = "dq2-ls '%s'" % pattern
    print 'cmd=%s' % cmd
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.split(os.linesep)
    
if __name__ == '__main__':
    ptag = 'data11_7TeV'
    stream = 'physics_Egamma'
    type = 'merge.AOD'
    reco_tag = 'f*'
    filename = '%s/work/GRL/data11_7TeV_Egamma.py' % os.environ['HOME']
    pattern = '%s.*.%s.%s.%s' % (ptag, stream, type, reco_tag)
    l = listDatasets(pattern)
    l.sort()
    f = open(filename, 'w')
    f.write('datasets = {\n')
    re0 = re.compile('%s\.(\d+)\.%s' % (ptag, stream))
    for i, x in enumerate(l):
        if len(x.strip()) == 0: continue
        mg = re0.search(x)
        run = 'X'*8
        tmp = '%d' % i
        n = len(tmp)
        if n <8: run = run[:8-n] + tmp
        else: run = tmp
        if mg:
            run = mg.group(1)
        f.write("    'run-%s' : '%s', \n" % (run, x))
    f.write('    }\n')
    f.close()


