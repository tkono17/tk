#!/usr/bin/python2.2

import sys
import os

python_path = os.getenv('PYTHONPATH')
install_dirs = python_path.split(':')
install_dir = install_dirs[0]

scripts = []
for i in range(1, len(sys.argv)):
    scripts.append(sys.argv[i])
    
if not os.path.isdir(install_dir):
    print 'Error: Directory ', install_dir, ' (in PYTHONPATH) does not exist'
    sys.exit(0)
for a in scripts:
    print 'script ', a

