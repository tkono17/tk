#!/usr/bin/env python
#-----------------------------------------------------------------
# mk_filelist.py
#-----------------------------------------------------------------

import os, sys
import re
import optparse
import commands

def createParser():
    p = optparse.OptionParser()
    p.add_option('-d', '--dir', dest='dir', type='string',
                 action='store', default='',
                 help='Path to the directory with files')
    p.add_option('-o', '--output-file', dest='output_file', type='string',
                 action='store', default='',
                 help='Output filelist file. Default is to write to stdout')
    p.add_option('-f', '--file', dest='file', type='string',
                 action='store', default='',
                 help='A file containing the sample->directories map for multiple samples. Useful when a sample has files in several directories or creating file list for many samples.')
    p.add_option('--output-dir', dest='output_dir', type='string',
                 action='store', default='.',
                 help='Directory to create output filelist files. Only used when running on multiple samples with -f option. For single sample, use -o instead')
    p.add_option('-p', '--pattern', dest='pattern', type='string',
                 action='store', default='.root',
                 help='Pattern to match to the file names (regex)')
    p.add_option('-b', '--base-dir', dest='base_dir', type='string',
                 action='store', default='',
                 help='Base directory to search for directories for files. Only matters when the --dir is specified as a relative path')
    p.add_option('-s', '--samples', dest='samples', type='string',
                 action='store', default='',
                 help='Comma separated list of sample names')

    p.usage += '\n'
    p.usage += "Examples: %prog -d <dir> -p '.root'\n"
    p.usage += "          %prog -d <dir> -p '.root' -s 'sample1,sample2'\n"
    p.usage += "          %prog -f files/ds.py --output-dir files/wjets -p 'JOB_OUTPUT' -b /pnfs/desy.de/atlas/dq2/atlaslocalgroupdisk/user/tkohno/data"
    
    return p

def usage(parser):
    parser.print_help()
    print "Examples: %s -d <dir> -p '.root'" % parser.prog

def list_directory(dir, pat):
    if dir == "": return []
    lines = []
    fstype=''
    if dir.find('/pnfs/') == 0 or dir.find(':/pnfs/') >= 0:
        # D-CACHE
        fstype = 'dcache'
        (status, output) = commands.getstatusoutput('dcls %s' % dir)
        if status == 0:
            lines = output.split(os.linesep)
        else:
            print 'Cannot list directory : %s' % dir
            print 'Error message: %s' % output
    else:
        # Normal file
        fstype = 'filesystem'
        if os.path.isdir(dir):
            lines = os.listdir(dir)
        else:
            print "list_directory: No directory '%s'" % dir
    x = []
    re0 = re.compile(pat)
    for line in lines:
        mg = re0.search(line)
        if mg:
            # print 'Matched : %s' % line
            x.append(line)
    return (x, fstype)

def createFileList(dir, pattern, fout=None):
    if dir == '' or pattern == '': return
    
    fsPrefix = {
        'filesystem': '',
        #'dcache': 'gsidcap://dcache-atlas-gsidcap.desy.de:22128',
        'dcache': 'dcap://dcache-ses-atlas.desy.de:22125',
        }
    (files, fstype) = list_directory(dir, pattern)
    prefix = ''
    if fstype in fsPrefix.keys(): prefix = fsPrefix[fstype]
    print 'Nfiles: %d' % len(files)
    files.sort()
    for f in files:
        fout.write('%s%s/%s\n' % (prefix, dir, f))

def createFileLists(file, pattern, samples, base_dir, output_dir):
    execfile(file)
    m = locals()['data_samples']
    keys = m.keys()
    keys.sort()
    def create(sample):
        fname = '%s/flist_%s.txt' % (output_dir, sample)
        fout = open(fname, 'w')
        n = len(m[sample])
        for (i, dir) in enumerate(m[sample]):
            fout.write('#------------------------------------------------\n')
            fout.write('# Sample %s [%d/%d]\n' % (sample, i, n))
            fout.write('#------------------------------------------------\n')
            createFileList(os.path.join(base_dir, dir), pattern, fout)
        print 'Created file list: %s' % fname

    print 'Nsamples=%d' % len(samples)
    print 'Nkeys=%d' % len(keys)
    if len(samples) > 0:
        for s in samples:
            if s not in keys: continue
            create(s)
    else:
        for k in keys:
            create(k)
    pass

                
if __name__ == '__main__':
    parser = createParser()
    (opts, args) = parser.parse_args()

    if hasattr(opts, 'help') and opts.help:
        parser.print_help()
        sys.exit(0)

    if opts.dir != '':
        fout = None
        if opts.output_file != '':
            print 'Writing the list of files to %s' % opts.output_file
            fout = open(opts.output_file, 'w')
        createFileList(os.path.join(opts.base_dir, opts.dir), opts.pattern,
                       fout)
        if fout != None: fout.close()
    elif opts.file != '':
        samples = filter(lambda x: x.strip()!='', opts.samples.split(','))
        createFileLists(opts.file, opts.pattern, samples,
                        opts.base_dir, opts.output_dir)
    if opts.base_dir != '':
        pass
    
