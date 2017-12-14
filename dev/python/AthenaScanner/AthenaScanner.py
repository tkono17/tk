#!/usr/bin/env python
#-------------------------------------------------------------------
# - Package:
#     - name
#     - version
#     - path
#     - is component library?
#     - components used : [Component]
# - Component:
#     - name
#     - type
#-------------------------------------------------------------------
import os, sys
import re, string

class Package:
    def __init__(self):
        self.mName = ''
        self.mPath = ''
        self.mVersion = ''
        self.mIsComponentLibrary = False
        self.mComponents = []
        self.mUses = []
        self.mDepth = 0
    def name(self):
        return self.mName
    def path(self):
        return self.mPath
    def version(self):
        return self.mVersion
    def depth(self):
        return self.mDepth
    def isComponentLibrary(self):
        return self.mIsComponentLibrary
    def allDependencies(self):
        return self.mUses
    def allDependencyNames(self):
        names = []
        for a in self.mUses:
            names.append(a.name())
        return names
    def allComponents(self):
        return self.mComponents
    def allComponentNames(self):
        names = []
        for a in self.mComponents:
            names.append(a.name())
        return names
    def algorithms(self):
        algos = []
        for c in self.mComponents:
            if c.isAlgorithm(): algos.append(c)
        return algos
    def services(self):
        svcs = []
        for c in self.mComponents:
            if c.isService(): svcs.append(c)
        return svcs
    def componentLibraries(self):
        libs = []
        for c in self.mUses:
            if c.isComponentLibrary(): libs.append(c)
        return libs
    def readNameVersionPath(self):
        cwd = os.getcwd()
        words = cwd.split(os.sep)
        name = words[-2]
        version = words[-1]
        path = cwd.replace(os.sep+words[-2]+os.sep+words[-1], '')
        return (name, version, path)
    def namepath(self):
        return self.mPath + os.sep + self.mName
    def abspath(self):
        namepath = self.namepath()
        cmtpaths = os.getenv('CMTPATH').split(':')
        for a in cmtpaths:
            a.strip('/')
            abspath = a + os.sep + namepath
            if os.path.isdir(abspath):
                os.chdir(abspath)
                for d in os.listdir('.'):
                    pattern = self.mVersion.replace('*', '\w*')
                    mg = re.search(pattern, d)
                    if mg: return abspath + os.sep + d
        return ''
    def cdHome(self):
        abspath = self.abspath()
        if len(abspath)>0: os.chdir(abspath)
        else:
            path = self.namepath()+os.sep+self.mVersion
            cmtpaths = os.getenv('CMTPATH').split(':')
            print 'Absolute path the package not found. ('+path+')'
            print 'CMTPATH: ', cmtpaths
    def printIt(self):
        (ndll, ncomp) = (0, 0)
        print '#--------------------------------------------------------'
        print self.mName + ': PATH='+self.mPath+' VERSION='+self.mVersion
        print 'Dependencies :'
        for p in self.componentLibraries():
            print '    '+p.name()
            ndll += 1
        print 'All components: '
        for a in self.allComponents():
            print "    %-40s %-20s %s" % (a.name(), a.type(), a.packageName())
            ncomp += 1
        print 'Number of DLLs : ', ndll
        print 'Number of Components: ', ncomp
        print '#--------------------------------------------------------'
    def createJobOptions(self, fname):
        file = open(fname, 'w')
        file.write('#-----------------------------------------------------\n')
        file.write('# Job options template\n')
        file.write('#-----------------------------------------------------\n')
        file.write('#\n')
        file.write('#-----------------------------------------------------\n')
        file.write('# Add DLLs\n')
        for a in self.componentLibraries():
            file.write("theApp.Dlls += ['"+a.name()+"']\n")
        file.write('#-----------------------------------------------------\n')
        file.write('#-----------------------------------------------------\n')
        file.write('# Create services\n')
        for a in self.services():
            file.write("theApp.ExtSvc += ['"+a.name()+"']\n")
        file.write('#-----------------------------------------------------\n')
        file.write('#\n')
        file.write('#-----------------------------------------------------\n')
        file.close()
    def setName(self, name):
        self.mName = name
    def setPath(self, path):
        self.mPath = path
    def setVersion(self, version):
        self.mVersion = version
    def setDepth(self, d):
        self.mDepth = d
    def setComponentLibrary(self, x):
        self.mIsComponentLibrary = x
    def addDependency(self, p):
        self.mUses.append(p)
    def setDependencies(self, ds):
        self.mUses = ds
    def addComponent(self, c):
        self.mComponents.append(c)
    def addComponents(self, ps):
        self.mComponents.extend(ps)
    def setComponents(self, ps):
        self.mComponents = ps

class Component:
    def __init__(self):
        self.mName = ''
        self.mType = '' # Algorithm, Service, Tool, AlgTool, Converter etc.
        self.mPackageName = ''
        self.mInstanceName = ''
    def name(self):
        return self.mName
    def type(self):
        return self.mType
    def packageName(self):
        return self.mPackageName
    def instanceName(self):
        return self.mInstanceName
    def isAlgorithm(self):
        return self.mType=='ALGORITHM'
    def isService(self):
        return self.mType=='SERVICE'
    def setName(self, name):
        self.mName = name
    def setType(self, type):
        self.mType = type
    def setPackageName(self, pn):
        self.mPackageName = pn
    def setInstanceName(self, n):
        self.mInstanceName = n

class Requirements:
    def __init__(self):
        self.mDependencies = []
    def addPackage(self,p):
        self.mDependencies.append(p)

#--------------------------------------------------------------------
# Functions
#--------------------------------------------------------------------
def scanRequirements():
    # print 'Scan requirements'
    req = Requirements()
    if not os.path.exists('requirements'): return req
    re_use = re.compile('use\s+(\w+)\s+([\w\*-]+)[\s+(\w*)]{0,1}')
    file = open('requirements', 'r')
    for line in file.readlines():
        # line = line[:-1]
        # line.strip()
        if len(line)==0 or line[0]=='#': continue
        mg = re_use.match(line)
        if mg:
            package = Package()
            words = line.split()
            package.setName(mg.group(1))
            package.setVersion(mg.group(2))
            if len(words)>3:
                package.setPath(words[3])
            req.addPackage(package)
    return req

def readLoadFile(fname):
    return

def readEntriesFile(fname, package_name):
    comp_info = []
    file = open(fname, 'r')
    # re_decfac = re.compile('DECLARE_([A-Z]+)_FACTORY\s*\(\s*(\w+)\s*\)')
    re_declare = re.compile('DECLARE_([A-Z]+)\s*\(\s*(\w+)\s*\)')
    re_declare_ns = re.compile('DECLARE_NAMESPACE_([A-Z]+)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)')
    for line in file.readlines():
        mg = re_declare.search(line)
        mg_ns = re_declare_ns.search(line)
        if mg:
            c = Component()
            # print mg.groups()
            c.setType(mg.group(1))
            c.setName(name = mg.group(2))
            c.setPackageName(package_name)
            comp_info.append(c)
        elif mg_ns:
            c = Component()
            # print mg_ns.groups()
            c.setType(mg_ns.group(1))
            c.setName(name = mg_ns.group(2)+'::'+mg_ns.group(3))
            c.setPackageName(package_name)
            comp_info.append(c)            
    return comp_info

def scanSrcComponents():
    # Must be called after changing directory to src/components of the package.
    # print 'Scan src/components'
    comp_info = []
    cwd = os.getcwd()
    cwd = cwd.replace(os.sep+'src'+os.sep+'components', '')
    words = cwd.split(os.sep)
    package_name = ''
    if len(words)>=2:
        package_name = words[-2]
        # print 'package name ', package_name
    else:
        print "Couldn't resolve the package name in directory: " + cwd
        return comp_info
    # re_load_match = re.compile(package_name+'\w*_load'+'\.\w*')
    # re_entries_match = re.compile(package_name+'\w*_entries'+'\.\w*')
    re_load_match = re.compile('\w*_load'+'\.\w*')
    re_entries_match = re.compile('\w*_entries'+'\.\w*')
    fname_load = ''
    fname_entries = ''
    filelist = os.listdir('.')
    for f in filelist:
        # print 'Directory listing: ', f
        mg = re_load_match.search(f)
        if mg: fname_load = mg.group(0)
        mg = re_entries_match.search(f)
        if mg: fname_entries = mg.group(0)
    if len(fname_load)==0 or len(fname_entries)==0:
        print 'Cannot find _load and _entries source files: ',package_name
        print 'src/components: ', filelist
        return comp_info
    comp_info = readEntriesFile(fname_entries, package_name)
    return comp_info
    
def scanPackage():
    cwd = os.getcwd()
    package = Package()
    words = cwd.split(os.sep)
    package.setName(words[-2])
    package.setVersion(words[-1])
    package.setPath(cwd.replace(words[-2]+os.sep+words[-1], ''))
    if os.path.isdir('cmt'):
        os.chdir('cmt')
        req = scanRequirements()
        for p in req.mDependencies:
            package.addDependency(p)
        os.chdir(cwd)
    else:
        print 'cmt directory not found under: ', cwd
    dirname_comp = 'src/components'
    if os.path.exists(dirname_comp) and os.path.isdir(dirname_comp):
        os.chdir(dirname_comp)
        comp_info = scanSrcComponents()
        if len(comp_info)>0:
            package.setComponentLibrary(True)
        package.addComponents(comp_info)
    #else:
    #    print 'No directory src/components found: ', os.getcwd()
    os.chdir(cwd)
    # package.printIt()
    return package

class PackageDependency:
    def __init__(self):
        self.mMaximumDepth = 0
        self.mPackageQueue = [] # array of dependant packages to be scanned
        self.mPackage = None
    def build(self):
        self.mPackage = Package()
        nvp = self.mPackage.readNameVersionPath()
        self.mPackage.setName(nvp[0])
        self.mPackage.setVersion(nvp[1])
        self.mPackage.setPath(nvp[2])
        self.mPackage.setDepth(0)
        self.mMaximumDepth = 0
        self.addToQueue(self.mPackage)
        while len(self.mPackageQueue)>0:
            package = self.mPackageQueue.pop()
            package.cdHome()
            # print 'Build package ',package.namepath(),'of depth: ', package.depth()
            self.buildPackage(package.depth())
    def getPackage(self):
        return self.mPackage
    def maximumDepth(self):
        return self.mMaximumDepth
    #-----------------------------------------------------------------
    # Below here are private functions
    #-----------------------------------------------------------------
    def addToQueue(self, package):
        # Add a new package at the front of the list. Then later pop the
        # list from the back, so using it as a FIFO.
        self.mPackageQueue[:0] = [package]
    def buildPackage(self, depth):
        # Must be executed at the directory of the package to be investigated
        deps = self.mPackage.allDependencyNames() # array of strings
        comps = self.mPackage.allComponentNames() # array of strings
        #print 'deps  : ', deps, 'depth=', depth
        #print 'comps: ', comps
        if depth > self.mMaximumDepth: self.mMaximumDepth = depth
        p = scanPackage()
        # p.printIt()
        for a in p.allDependencies():
            if not a.name() in deps:
                #print 'Add new package: ', a.name()
                a.setDepth(depth+1)
                deps.append(a.name())
                self.mPackage.addDependency(a)
                self.addToQueue(a)
            #else:
            #    print 'Package '+a.name()+' already exists'
        for a in p.allComponents():
            if not a.name() in comps:
                comps.append(a.name())
                self.mPackage.addComponent(a)
        for pp in self.mPackage.allDependencies():
            if pp.name()==p.name():
                pp.setComponentLibrary(p.isComponentLibrary())
                pp.setDependencies(p.allDependencies())
                pp.setComponents(p.allComponents())
        #print 'deps after : ', deps, 'depth=',depth
        #print 'comps after: ', comps
        
if __name__=='__main__':
    # package = scanPackage()
    pb = PackageDependency()
    pb.build()
    pb.getPackage().printIt()
    print 'Maximum depth was', pb.maximumDepth()
    pb.getPackage().createJobOptions('/space/tkohno/work/TrigConf/joboptions.py')
    
