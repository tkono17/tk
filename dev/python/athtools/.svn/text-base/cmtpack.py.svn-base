#!/usr/bin/env python
import os
import sys
import re

gExcludeDirs = ['InstallArea', 'installed', 'doc', 'CVS']
# , 'share', 'src', 'cmt'
gGeneratedDirs = ['CVS', 'genConf', 'rootmap', 'pool', 'pool_plugins', 'dict' ]

class Package:
    def __init__(self):
        self.mName = ''
        self.mVersion = ''
        self.mCmtBasePath = ''
        self.mRelPath = ''
        self.mAbsPath = ''
    def __init__(self, name, version, path):
        self.mName = name
        self.mVersion = version
        self.mCmtBasePath = ''
        self.mRelPath = ''
        self.mAbsPath = os.path.abspath(path)
        for cmt_path in get_cmtpath():
            mg = re.match('(^'+cmt_path+')', self.mAbsPath)
            if mg!=None:
                mCmtBasePath = cmt_path
                mRelPath = re.sub(cmt_path+'/', '', self.mAbsPath)
    def printIt(self):
        print "%-30s %-40s %-50s" % (self.mName, self.mVersion, self.mAbsPath)

def matches_build_dir(dir):
    if re.search('-slc[0-9]-gcc[0-9]*-', dir):
        return True
    else:
        return False

def package_sources(dir):
    subdirs = []
    curdir = os.getcwd()
    bname = os.path.basename(dir)
    if os.path.exists(dir) and os.path.isdir(dir):
        os.chdir(dir)
        for s in os.listdir(dir):
            include_it = True
            if matches_build_dir(s) or s in gGeneratedDirs:
                include_it = False
                continue
            if os.path.isdir(s):
                subs2 = os.listdir(s)
                includes_link = False
                includes_obj = False
                for sub2 in subs2:
                    p = os.path.join(s, sub2)
                    if os.path.islink(p):
                        includes_link = True
                        break
                    if re.search('\.o$', p):
                        includes_obj = True
                        break
                if (includes_link and s!='src' and s!=bname) or includes_obj:
                    print 'Warning: Not a source directory? %s (%s)' \
                          % (s, dir)
                    include_it = False
            if include_it:
                subdirs.append(s)
    os.chdir(curdir)
    return subdirs

def get_cmtpath():
    tmp = os.getenv('CMTPATH')
    if tmp=='': return []
    return tmp.split(':')

def is_package_dir(dir='.'):
    p = os.path.join(dir, 'cmt')
    req = os.path.join(p, 'requirements')
    if os.path.exists(dir) and 'cmt' in os.listdir(dir) and \
           os.path.isdir(p) and os.path.exists(req):
        return True
    else:
        return False

def sub_packages(dir='.'):
    global gExcludeDirs
    ret = []
    if os.path.exists(dir):
        cmtconfig = os.getenv('CMTCONFIG')
        for s in os.listdir(dir):
            fp = os.path.join(dir, s)
            if os.path.isdir(fp) and not os.path.islink(fp) and \
                   not s in gExcludeDirs and \
                   not re.match('NICOS_', s) and \
                   not matches_build_dir(s):
                ret.append(s)
    return ret

def package_name(dir='.'):
    if not is_package_dir(dir): return ''
    curdir = os.getcwd()
    os.chdir(dir)
    name = os.path.basename(os.getcwd())
    os.chdir(curdir)
    return name

def package_version(dir='.'):
    if not is_package_dir(dir): return ''
    curdir = os.getcwd()
    os.chdir(dir)
    ver = ''
    if os.path.exists('cmt/version.cmt'):
        f = open('cmt/version.cmt', 'r')
        ver = f.readline()
        if ver[-1]=='\n': ver = ver[:-1]
    os.chdir(curdir)
    return ver
    
def package_path(dir='.'):
    if not is_package_dir(dir): return ''
    curdir = os.getcwd()
    os.chdir(dir)
    path = os.path.dirname(os.getcwd())
    for cmtpath in get_cmtpath():
        if re.match(cmtpath, path):
            path = re.sub(cmtpath+'/', '', path)
            break
    os.chdir(curdir)
    return path

def find_package(expr, dir):
    packs = []
    if is_package_dir(dir):
        name = package_name(dir)
        if re.match(expr, name):
            p = Package(name, package_version(dir), package_path(dir))
            packs.append(p)
    for p in sub_packages(dir):
        tmp = find_package(expr, os.path.join(dir, p))
        if len(tmp)>0: packs.extend(tmp)
    return packs

def find_package_all(expr):
    curdir = os.getcwd()
    packs = []
    for p in get_cmtpath():
        print 'Looking in cmtpath = ' + p
        os.chdir(p)
        tmp = find_package(expr, p)
        if len(tmp)>0: packs.extend(tmp)
    os.chdir(curdir)
    return packs

def all_packages_under(dir):
    curdir = os.getcwd()
    packs = []
    if os.path.exists(dir) and os.path.isdir(dir):
        os.chdir(dir)
        if is_package_dir(dir):
            packs.append(Package(package_name(dir), package_version(dir), dir))
        else:
            subdirs = sub_packages(dir)
            for subdir0 in subdirs:
                packs.extend(all_packages_under(os.path.abspath(subdir0)))
        os.chdir(curdir)
    else:
        return []
    return packs

def all_packages():
    curdir = os.getcwd()
    packs = []
    for p in get_cmtpath():
        print 'Looking in cmtpath = ' + p
        packs.extend(all_packages_under(p))
    os.chdir(curdir)
    return packs

if __name__=='__main__':
    if len(sys.argv)==1:
        packs = all_packages()
        print 'Number of all packages :', len(packs)
        for (n, a) in enumerate(packs):
            print "%04d : %-s" % (n, a.mAbsPath)
    elif sys.argv[1]=='-h':
        print 'Usage: ', sys.argv[0], ' <package_name>'
    elif len(sys.argv)>1:
        package_sources(sys.argv[1])
        sys.exit(0)
        print 'Finding packages matching ', sys.argv[1]
        a = find_package_all(sys.argv[1])
        print 'Number of matched packages: ', len(a)
        if len(a)>0:
            for b in a:
                b.printIt()
