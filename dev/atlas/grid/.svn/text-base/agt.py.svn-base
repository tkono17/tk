#!/usr/bin/env python

#----------------------------------------------------------------------
# atg.py
#--------
# ATLAS Grid Tools
#----------------------------------------------------------------------
import os, sys
import re
import commands
import tklog

agtlog = 'logs/agt.log'

FileList_SiteLFNPFN = 'fileList_SiteLFNPFN.txt'

class AtlasTiers:
    def __init__(self):
        if '.' not in os.environ['PYTHONPATH'].split(':'):
            os.environ['PYTHONPATH'] = '.:' + os.environ['PYTHONPATH']
        import TiersOfATLASCache as A
        self.ToA = A
        self.tier1s = []
    def info(self):
        return self.ToA
tierInfo = AtlasTiers().info()

SitesInPriority = (
    'CERN', 
    'CNAF', 
    'LYON', 
    'FZK', 
    'BNL', 
    'RAL', 
    'ASGC', 
    'NIKHEF', 
    'TRIUMF', 
    'MILANO', 
    'NAPOLI', 
    'NDGFT1', 
    'PIC', 
    'SARA', 
    )

def orderSites(site1, site2):
    all_sites = list(SitesInPriority)    
    i1 = all_sites.index(site1)
    i2 = all_sites.index(site2)
    if i1>=0 and i2>=0:
        if i1<i2: return -1
        elif i1>i2: return 1
        else: return 0
    elif i1>=0 and i2<0:
        return -1
    elif i1<0 and i2>=0:
        return 1
    else:
        return 0

def sortSites(sites):
    sites_ng = []
    for s in filter(lambda x: x not in SitesInPriority, sites):
        print 'Site %s not in the priority list' % s
        sites_ng.append(s)
    ret = filter(lambda x: x in SitesInPriority, sites)
    ret.sort(orderSites)
    ret.extend(sites_ng)
    ret.remove('BNL')
    return ret

def listFilesAndSites(dataset_name):
    """List all files and sites which have some files of a given dataset."""
    command = 'dq2_ls -g -r %s' % dataset_name
    status, output = commands.getstatusoutput(command)
    if status != 0:
        print 'Error executing "%s"', command
    files=[]
    sites=[]
    re_site = re.compile('\s*([\w]+)\s+-\s+[\w]*[\w\s]*Replica')
    for line in output.split('\n'):
        if len(line)==0 or line[0]=='#': continue
        if len(line)>0 and line.find(dataset_name)==0:
            continue
        elif line.find(dataset_name)!=-1:
            files.append(line.strip(' '))
        else:
            mg = re_site.match(line)
            if mg:
                sites.append(mg.group(1))
    return (files, sites)
        
def listFilesInDataset(dataset_name):
    """List all files (LFN) in the given DQ2 dataset."""
    (files, sites) = listFilesAndSites(dataset_name)
    return files

def createFilelistForSite(dataset_name, files, site, ignorelist=[]):
    """Create a filelist for a given dataset. The list contains the 
    logical file name (LFN), physical filename (PFN) for each file.
    """
    # file info (site, lfn, pfn)
    files = []
    ignore_lfns = map(lambda x: x[1], ignorelist) # list of LFN
    # Look for PFN and make a map LFN->PFN
    lfn_pfn = {}
    command = 'dq2_ls -f -p -s %s %s' % (site, dataset_name)
    status, output = commands.getstatusoutput(command)
    if status != 0:
        print 'Error executing %s' % command
    else:
        for line in output.split('\n'):
            if len(line)==0: continue
            pfn = line.strip(' ')
            lfn = os.path.basename(pfn)
            if lfn not in ignore_lfns:
                lfn_pfn[lfn] = pfn
    # Look for LFN
    command = 'dq2_ls -f -s %s %s' % (site, dataset_name)
    status, output = commands.getstatusoutput(command)
    if status != 0:
        print 'Error executing %s' % command
    else:
        re_fn = re.compile('\s+[^\s]+')
        for line in output.split('\n'):
            if len(line)==0: continue
            lfn = line.strip(' ')
            if re_fn.match(line) and lfn not in ignore_lfns:
                pfn = ''
                if lfn in lfn_pfn.keys(): pfn = lfn_pfn[lfn]
                #else:
                #    print 'Cannot find PFN for LFN: %s (mapsize=%d)' %\
                #          (lfn, len(lfn_pfn))
                files.append( (site, lfn, pfn))
    return files

def createFilelist(dataset_name, files, sites):
    """Create a filelist for a given dataset. The list contains the 
    logical file name (LFN), physical filename (PFN) for each file.
    """
    filelist=[]
    for site in sites:
        files = createFilelistForSite(dataset_name, file, site)
        filelist.extend(files)
        print 'Number of files at site %s is %d' % (site, len(files))
    return filelist
    
def createFilelistForDS(dataset_name, fname_out=FileList_SiteLFNPFN):
    """Create a filelist for a given dataset. The list contains the 
    logical file name (LFN), physical filename (PFN) for each file.
    """
    (files, sites) = listFilesAndSites(dataset_name)
    filelist = createFilelist(dataset_name, files, sortSites(sites))
    fout = open(fname_out, 'w')
    format = '%%-10s %%-%ds %%-s\n' % len(dataset_name)
    for slp in filelist:
        fout.write(format % slp)
    fout.close()

def createFilelistToSubmit(filelist_name, out_name):
    fin = open(filelist_name, 'r')
    re_slp = re.compile('([^ ]+)\s+([^ ]+)\s+([^ ]+)')
    re_sl = re.compile('([^ ]+)\s+([^ ]+)')
    fout = open(out_name, 'w')
    #
    lfns = []
    site=''
    lfn=''
    pfn=''
    #
    for line in fin.readlines():
        if len(line)>0: line = line[:-1]
        line = line.strip()
        mg = re_slp.match(line)
        if mg:
            (site, lfn, pfn) = mg.groups()
        else:
            mg = re_sl.match(line)
            if mg: (site, lfn) = mg.groups()
        if lfn not in lfns:
            lfns.append(lfn)
            fout.write(line+'\n')
    fin.close()
    fout.close()

def readInFilelist(fname_in):
    slp = []
    fin = open(fname_in, 'r')
    for line in fin.readlines():
        if len(line)>0: line = line[:-1]
        words = line.split()
        if len(words)==3:
            slp.append(words)
    return slp

def getSiteCEs(site_name):
    """Select CE for Site."""
    sites = findCloseSites(site)
    CEs = []
    for s in sites:
        if s in tierInfo.sites.keys():
            sinfo = tierInfo.sites[s]
            if 'ce' in sinfo.keys():
                ce = CEs.extend(sinfo['ce'])
    return CEs

def getSiteSRM(site_name):
    srm=''
    ce = ''
    if site_name in tierInfo.sites.keys():
        site = tierInfo.sites[site_name]
        if 'srm' in site.keys(): return site['srm']
    return ''

def getSiteSRMHost(site_name):
    protocol=''
    srmhost=''
    if site_name in tierInfo.sites.keys():
        site = tierInfo.sites[site_name]
        if 'srm' in site.keys():
            mg = re.match('(\w+)://([^/]+)', site['srm'])
            return mg.group(1)
            #print 'SRMHost: protocol=%s, host=%s' % mg.groups()
    return ''

def siteExistsInSite(site, site0):
    """true/false"""
    ret = False
    if site==site0: ret = True
    if site0 in tierInfo.topology.keys():
        sites = tierInfo.topology[site0]
        if site in sites:
            ret = True
        else:
            for s1 in sites:
                status = siteExistsInSite(site, s1)
                if status:
                    ret = True
                    break
    return ret

def findSitesUnder(site0, recursive=True):
    """Finds sites under the specified site"""
    ret=[]
    if site0 in tierInfo.topology.keys():
        sites = tierInfo.topology[site0]
        ret.extend(sites)
        if recursive:
            for s1 in sites:
                ret.extend(findSitesUnder(s1))
    return ret
    
def findCloseSites(site0, recursive=True):
    """Finds sites under the specified site"""
    ret=[]
    topSites = tierInfo.closeSitesTopology.keys()
    topSites.remove('TIER1S')
    t1 = ''
    for s1 in topSites:
        if siteExistsInSite(site0, s1):
            t1 = s1
            break
    if t1=='':
        print 'Cannot find T1 of this site ', site0
    if t1!='':
        ret.extend(findSitesUnder(t1))
    toRemove=['TIER0TAPE', 'TIER0DISK' ] # , 'CERNPROD']
    ret = filter(lambda x: not (x in toRemove or \
                                x.find('TAPE')!=-1 or \
                                x.find('TIER0')!=-1), ret)
    ret = filter(lambda x: x in tierInfo.sites.keys(), ret)
    return ret

def decodeURL(url):
    # mg = re.match('(\w+)://([^/:]+)(?:[:]d+)([\w.-_/]+)', url)
    mg = re.match('(\w+)://([^/]+)([\w.-_/]+)', url)
    if mg:
        return mg.groups()
    else:
        return ('', '', '')

def findLFCHost(site):
    lfc = ''
    ok = False
    for (lfc2, s2) in tierInfo.catalogsTopology.iteritems():
        if ok: break
        for s in s2:
            # print 'checking %s against %s' % (s, site)
            sites = [s]
            sites.extend(findSitesUnder(s))
            if site in sites:
                lfc = decodeURL(lfc2)[1]
                lfc = lfc.rstrip(':')
                ok = True
                break
    return lfc

def selectCEForSite(CEs):
    """Select CE for Site."""
    ce = ''
    if len(CEs)>0: ce = CEs[0]
    ce='ce101.cern.ch:2119/jobmanager-lcglsf-grid_2nh_atlas'
    # ce='gridce.pi.infn.it:2119/jobmanager-lcglsf-atlas'
    # ce='ce05-lcg.cr.cnaf.infn.it:2119/jobmanager-lcglsf-atlas'
    #ce='cclcgceli05.in2p3.fr:2119/jobmanager-bqs-atlas_long'
    #ce='mars-ce2.mars.lesc.doc.ic.ac.uk:2119/jobmanager-sge-24hr'
    #ce='ce05-lcg.cr.cnaf.infn.it:2119/jobmanager-lcglsf-atlas'
    return ce

def pfnToSURL(pfn, site):
    sites = findCloseSites(site)
    surl = ''
    for s in sites:
        if 'srm' in tierInfo.sites[s].keys():
            srm = tierInfo.sites[s]['srm']
            (protocol, host, path) = decodeURL(srm)
            if re.match(path, pfn):
                surl = '%s://%s%s' % (protocol, host, pfn)
            i = pfn.find('/dq2/')
            if i >= 0:
                surl = 'lfn:/grid/atlas' + pfn[i:]
    return surl

def createJobInfo(site, input_lfns, input_pfns):
    finfo = open('jobinfo.py', 'w')
    finfo.write("Site = '%s'\n" % site)
    # LFN
    s = 'InputLFNs = [\n'
    for a in input_lfns:
        s += ("  '%s',\n" % a)
    s += ']'
    finfo.write(s+'\n')
    # PFN
    s = 'InputPFNs = [\n'
    for a in input_pfns:
        s += ("  '%s',\n" % a)
    s += ']'
    finfo.write(s+'\n')
    # CE
    sites2 = findCloseSites(site)
    s = 'CEs = [\n'
    for s2 in sites2:
        if s2 in tierInfo.sites.keys() and 'ce' in tierInfo.sites[s2].keys():
            for ce in tierInfo.sites[s2]['ce']:
                s += ("  '%s',\n" % ce)
    s += ']\n'
    finfo.write(s+'\n')
    finfo.close()

def jobID():
    return os.path.basename(os.getcwd())

def setupJobs(slp=None, joblist_file='joblist'):
    """slp: [site, LFN, PFN]"""
    ret_jobids=[]
    nfiles_per_job=10
    if slp==None:
        slp = readInFilelist('tosubmit.txt')
    sites=[]
    joblist=[]
    for a in slp:
        if a[0] not in sites: sites.append(a[0])
    for site in sites:
        # Split input files into pieces to create subjobs
        files = filter(lambda x: x[0]==site, slp)
        lfnpfns = map(lambda x: x[1:3], files)
        njobs = len(lfnpfns)/nfiles_per_job
        if (len(lfnpfns) % nfiles_per_job) != 0: njobs += 1
        for ijob in range(njobs):
            jobid = '%s.%d' % (site,  ijob)
            joblist.append(jobid)
            input_lfns = []
            input_pfns = []
            for i in range(nfiles_per_job):
                j = ijob*nfiles_per_job + i
                if j<len(lfnpfns):
                    input_lfns.append(lfnpfns[i][0])
                    input_pfns.append(lfnpfns[i][1])
            if not (os.path.exists(jobid) and os.path.isdir(jobid)):
                print 'Make directory: %s' % jobid
                os.mkdir(jobid)
            curdir=os.getcwd()
            os.chdir(jobid)
            createJobInfo(site, input_lfns, input_pfns)
            os.chdir(curdir)
    fout = open(joblist_file, 'w')
    for j in joblist:
        fout.write('%s\n' % j)
    fout.close()

def applyHook(template, hooks, newfile):
    """Apply hooks into the template file using insert_in_tag.py"""

def createHooks():
    """Create hooks file from the job_info file produced after setupJobs()"""
    
    
def applyHooks(jc):
    """Apply hooks for JDL, JO, script."""
    jc.JobOptions.update('^#JO-HOOK')
    jc.JdlFile.update('^#JDL-HOOK')
    jc.Script.update('^#SCRIPT-HOOK')

def writeJOHooks(fout, lfns):
    """Write out hooks needed for the jobOptions file"""
    prefix='#JO-HOOK'
    fout.write('%s-InputFiles_begin\n' % prefix)
    fout.write('EvtMax = -1\n')
    fout.write('InputFiles = [\n')
    for f in lfns:
        # if not os.path.exists(fp) or os.stat(fp).st_size==0: continue
        fout.write("  'LFN:%s',\n" % f)
    fout.write(']\n')
    fout.write('%s-InputFiles_end\n\n' % prefix)

def writeJDLHooks(fout, ce, fin_name):
    """Write out hooks needed for the JDL script"""
    prefix='#JDL-HOOK'
    #
    req=''
    if os.path.exists(fin_name):
        fin = open(fin_name, 'r')
        for line in fin.readlines():
            line = line[:-1]
            mg = re.search('Requirements\s*=\s*([^\s]+.*)', line)
            if mg:
                req += mg.group(1)
                i = req.find(';')
                if i>=0: req = req[:i]
    fout.write('%s-CE_begin\n' % prefix)
    if len(req)>0: req += ' && '
    req += 'other.CEId=="%s";\n' % ce
    fout.write('Requirements = ' + req)
    fout.write('%s-CE_end\n\n' % prefix)

def writeScriptHooks(fout, surls, lfchost, jo_name, job_id):
    """Write out hooks needed for the executable script"""
    prefix = '#SCRIPT-HOOK'
    #
    fout.write('%s-InputFiles_begin\n' % prefix)
    fout.write('InputFiles=(\n')
    for surl in surls:
        fout.write('  %s\n' % surl)
    fout.write(')\n')
    fout.write('%s-InputFiles_end\n\n' % prefix)
    #
    fout.write('%s-LFC_HOST_begin\n' % prefix)
    fout.write('export LFC_HOST=%s\n' % lfchost)
    fout.write('%s-LFC_HOST_end\n\n' % prefix)
    #
    fout.write('%s-JobOptionsFile_begin\n' % prefix)
    fout.write('JobOptionsFile=%s\n' % jo_name)
    fout.write('%s-JobOptionsFile_end\n\n' % prefix)
    #
    fout.write('%s-JobID_begin\n' % prefix)
    fout.write('JobID=%s\n' % job_id)
    fout.write('%s-JobID_end\n\n' % prefix)


def listOfJobs(joblist_file='joblist'):
    output = open(joblist_file, 'r')
    jobs=[]
    for line in output.readlines():
        line = line[:-1]
        if line.startswith('#'): continue
        if len(line)>0: jobs.append(line)
    output.close()
    return jobs

def prepareJob(jc):
    # expects input files in jobinfo file
    jobid = jobID()
    print 'Preparing job for %s using jobinfo.py' % jobid
    #
    f_jobinfo = open('jobinfo.py', 'r')
    exec f_jobinfo.read()
    # Variables Site, InputLFNs, InputPFNs should be defined here.
    if os.path.exists(jc.Hooks.name()):
        os.remove(jc.Hooks.name())
    f_hooks = open(jc.Hooks.name(), 'w')
    # 1. Hooks for jobOptions
    lfns = []
    writeJOHooks(f_hooks, InputLFNs)
    # 2. Hooks for script
    pfns = []
    for pfn in InputPFNs:
        pfn = pfnToSURL(pfn, Site)
        # print pfn, '->', pfn
        pfns.append(pfn)
    lfchost = findLFCHost(Site)
    writeScriptHooks(f_hooks, pfns, lfchost, jc.JobOptions.name(), jobid)
    # 3. Hooks for JDL
    ce = jc.CE.name()
    if ce=='': ce = selectCEForSite(CEs)
    writeJDLHooks(f_hooks, ce, jc.JdlFile.template())
    f_hooks.close()
    # 4. Apply hooks
    applyHooks(jc)
    return

def loopJobs(jc, joblist_file, funcForJob):
    """A"""
    jobs = listOfJobs(joblist_file)
    curdir=os.getcwd()
    for job in jobs:
        os.chdir(job)
        funcForJob(jc)
        os.chdir(curdir)
    
def runJob(jc):
    """A"""
    out, err = 'runjob.out', 'runjob.err'
    jobid_out = 'jobid'
    print 'Submitting job %s' % (os.path.basename(os.getcwd()))
    if os.path.exists(out): os.remove(out)
    if os.path.exists(err): os.remove(err)
    if os.path.exists(jobid_out):
        os.system('cat %s >> %s.sav' % (jobid_out, jobid_out))
        os.remove(jobid_out)
    # print 'Submitting job %s to CE=%s' % (bbb)
    command = 'edg-job-submit --vo atlas -o %s %s 1>>%s 2>>%s' % \
              (jobid_out, jc.JdlFile.name(), out, err)
    if jc.JobType.name():
        if os.path.exists(jc.RunScript.name()):
            os.chmod(jc.RunScript.name(), 0744)
            command = '%s 1>>%s 2>>%s &' % (jc.RunScript.name(), out, err)
        else:
            return
    (status, output) = tklog.system(command, agtlog)
    if status != 0:
        print '*** Error while submitting job %s. Check the output %s/%s' %\
              (os.path.basename(os.getcwd()), os.getcwd(), out)

def prepareJobs(jc, joblist_file):
    loopJobs(jc, joblist_file, prepareJob)

def runJobs(jc, joblist_file):
    """A"""
    loopJobs(jc, joblist_file, runJob)

def statusJob(jc):
    """A"""
    out, err = 'statusjob.out', 'statusjob.err'
    jobid_out = 'jobid'
    if os.path.exists(out): os.remove(out)
    if os.path.exists(err): os.remove(err)
    if not os.path.exists(jobid_out):
        print 'Cannot find jobid file: %s' % jobid
    command = 'edg-job-status -i %s 1>>%s 2>>%s' % (jobid_out, out, err)
    tklog.system(command, agtlog)
    job_id=''
    job_status = ''
    job_ce = ''
    output = open(out, 'r')
    re_jobid = re.compile('^Status info for the Job :\s*([^\s]+)')
    re_status = re.compile('^Current Status:\s*(\w+)')
    re_ce = re.compile('^Destination:\s*([^\s]+)')
    for line in output.readlines():
        if line.startswith('#'): continue
        line = line[:-1]
        mg1 = re_jobid.match(line)
        mg2 = re_status.match(line)
        mg3 = re_ce.match(line)
        if mg1: job_id = mg1.group(1)
        if mg2: job_status = mg2.group(1)
        if mg3: job_ce = mg3.group(1)
    output.close()
    bbb=os.path.basename(os.getcwd())
    print 'Status of job %s : %s (CE=%s)' % (bbb, job_status, job_ce)
    return job_status

def statusJobs(jc, joblist_file):
    """A"""
    loopJobs(jc, joblist_file, statusJob)

def getJob(jc):
    """A"""
    jobid_out = 'jobid'
    jobid = os.path.basename(os.getcwd())
    if not os.path.exists(jobid_out):
        print 'Cannot find jobid file: %s' % jobid
    if statusJob(jc) == 'Done':
        print 'Retrieving output of job %s' % jobid
        out, err = 'getjob.out', 'getjob.err'
        if os.path.exists(out): os.remove(out)
        if os.path.exists(err): os.remove(err)
        command = 'edg-job-get-output -i %s -dir . 1>>%s 2>>%s' % \
                  (jobid_out, out, err)
        (status, output) = tklog.system(command, agtlog)
        if status != 0:
            print 'Error while getting job output. Check output at %s' % out
            return
        output = open(out, 'r')
        check_it=False
        dir=''
        for line in output.readlines():
            line = line[:-1]
            if check_it:
                dir = line.strip()
                check_it = False
                break
            elif line.find('have been successfully retrieved and stored')>=0:
                check_it = True
                continue
        if len(dir)>0:
            print '  --> Job output stored in directory %s' % dir
            
            
def getJobs(jc, joblist_file):
    """A"""
    loopJobs(jc, joblist_file, getJob)

def runLCG(jc):
    """Submit the job to LCG"""
    
def runLocal(jc):
    opt = ''
    command = 'athena.py %s %s' % (opt, jc.JobOptions.filename())
    os.system(command)
    
def siteCE(site_name):
    srm=''
    ce = ''
    if site_name in tierInfo.sites.keys():
        site = tierInfo.sites[site_name]
        if 'srm' in site.keys(): print 'SRM: ', site['srm']
        if 'ce' in site.keys(): print 'CE : ', site['ce']

def siteSRM(site_name):
    srm=''
    ce = ''
    if site_name in tierInfo.sites.keys():
        site = tierInfo.sites[site_name]
        if 'srm' in site.keys(): print 'SRM: ', site['srm']
        if 'ce' in site.keys(): print 'CE : ', site['ce']

def siteSRMHost(site_name):
    protocol=''
    srmhost=''
    if site_name in tierInfo.sites.keys():
        site = tierInfo.sites[site_name]
        if 'srm' in site.keys():
            mg = re.match('(\w+)://([^/]+)', site['srm'])
            print 'SRMHost: protocol=%s, host=%s' % mg.groups()
        
def printSiteInfo():
    for name, site in tierInfo.sites.iteritems():
        print '#- %s -----------------------------------' % name
        for k,v in site.iteritems():
            print '   %-20s: %20s' % (k, v)

if __name__=='__main__':
    # dataset_name='trig1_misal1_csc11.005105.PythiaWmunu.recon.AOD.v12000601'
    dataset_name='misal1_valid1.005145.PythiaZmumu.digit.RDO.v13001001'
    dataset_name='valid3_valid1.005145.PythiaZmumu.digit.RDO.v13001001'
    dataset_name='misal1_valid1.005145.PythiaZmumu.digit.RDO.v13001001'
##     (files, sites) = listFilesAndSites(dataset_name)
##     print '%d files found' % len(files)
##     print '%d sites found' % len(sites)
##     for s in sites:
##         print s
    # printSiteInfo()
    #
    createFilelistForDS(dataset_name, FileList_SiteLFNPFN)
    createFilelistToSubmit(FileList_SiteLFNPFN, 'tosubmit.txt')
    setupJobs()
    pass

