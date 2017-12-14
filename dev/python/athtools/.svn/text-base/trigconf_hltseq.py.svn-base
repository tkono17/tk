#!/usr/bin/env python
#----------------------------------------------------------------------
# trigconf_htlseq.py
# ------------------
# Dumps the HLT sequences in a nice format from the XML file.
#----------------------------------------------------------------------

import os, sys
import re
import xml.dom.minidom


def seqOrder(seq1, seq2):
    x = seq1[2]
    y = seq2[2]
    def aaa(x):
        if x.startswith('EF')or x=='Zee' or x=='Jpsiee': return 3
        elif x.startswith('L2'): return 2
        else: return 1
    getlevel = aaa
    ix = getlevel(x)
    iy = getlevel(y)
    if ix < iy: return -1
    elif ix == iy:
        if seq1[0] < seq2[0]: return -1
        elif seq1[0]==seq2[0] and seq1[2] < seq2[2]: return -1
        elif seq1[0]==seq2[0] and seq1[2] == seq2[2]: return 0
        else: return 1
    else: return 1

def printSeqs(seq_reps):
    seq_reps.sort(seqOrder)
    w1 = max(map(lambda x: len(x[0]), seq_reps))
    w2 = max(map(lambda x: max(map(lambda y: len(y), x[1].split(' '))),
                 seq_reps))
    w3 = max(map(lambda x: len(x[2]), seq_reps))
    format = '%%-%ds %%-%ds %%-%ds' % (w1, w2, 23)
    for a in seq_reps:
        input = a[0]
        output = a[2]
        algs = a[1].split(' ')
        if len(algs)==0: algs = '---'
        alg_offset = ''
        for alg in algs:
            fmt = format
            if output == '':
                fmt = '%%-%ds %%-%ds' % (w1, w2)
                print fmt % (input, alg_offset+alg)
            else:
                print fmt % (input, alg_offset+alg, output)
                input = ''
                output = ''
                alg_offset += '  '

def seqAlgs(seq):
    ret = []
    algs = seq[1].split(' ')
    for a in algs:
        b = a.split('/')
        if len(b)>0: ret.append(b[0])
    return ret

def seqType(seq):
    algs = seqAlgs(seq);
    ret = ''
    for a in algs:
        ret += '->' + a
    return ret

def allSeqTypes(seqs):
    ret = {}
    for s in seqs:
        type = seqType(s)
        if type in ret.keys():
            ret[type] += 1
        else:
            ret[type] = 1
    return ret

def seqTypeInstance(seq):
    ret = ()
    type = seqType(seq)
    names = []
    algs = seq[1].split(' ')
    for a in algs:
        tn = a.split('/')
        if len(tn)>1: names.append(tn[1])
        else: names.append(tn[0])
    return (type, names)

def allSeqTypeInstances(seqs, type):
    tns = []
    for s in seqs:
        t = seqType(s)
        if not t == type: continue
        tn = seqTypeInstance(s)
        tns.append(tn[1])
    return tns

def checkAlgNames(seqNames):
    """Input: seqNames = [ [ algo1, algo2, ...], [algo1, algo2, ... ]]
    Output:
    [ (commonPart, [algoName1, algoName2, ...],
    (commonPart, [algoName1, algoName2, ...],
    (commonPart, [algoName1, algoName2, ...],
    ]
    """
    def findFirstDiff(s1, s2):
        n = min(len(s1), len(s2))
        i = 0
        for i in range(n):
            if s1[i] != s2[i]: return i
        return n
    n = len(seqNames[0])
    base_names = ['?']*n
    real_names = [ 1 ]*n
    for i in range(n): real_names[i] = []
    for s in seqNames:
        for i in range(n):
            idiff = findFirstDiff(base_names[i], s[i])
            if base_names[i] == '?': base_names[i] = s[i]
            else: base_names[i] = base_names[i][:idiff]
            if idiff < len(s[i]) and s[i] not in real_names[i]:
                real_names[i].append(s[i])
    names = []
    for i in range(n):
        names.append( (base_names[i], real_names[i]))
    return names
        
def printSeqsPerType(seq_reps):
    unique_seqs = allSeqTypes(seq_reps)
    kkk = unique_seqs.keys()
    # kkk.sort()
    for type in kkk:
        offset = ''
        c = type.split('->')
        all_names = allSeqTypeInstances(seq_reps, type)
        common_real_names = checkAlgNames(all_names)
        print '#-------------------------------------------------------'
        print '# Sequence type: ' + type + ' (x ' + str(unique_seqs[type]) + ')'
        print '#-------------------------------------------------------'
        for b in c:
            if len(b)==0: continue
            line = offset+b
            print line
            offset += '  '
        xxx = 0
        for crn in common_real_names:
            tmp = max(map(lambda x: len(x), crn[1]))
            if xxx < tmp: xxx = tmp
        fmt2 = ' --- %%-%ds %%s' % xxx
        for crn in common_real_names:
            tmp = '['
            for c in crn[1]:
                tmp += c.replace(crn[0], '') + ', '
            tmp += ']'
            print fmt2 % (crn[0], tmp)
    print 'Number of unique sequences: ', len(unique_seqs)

def readSeqReps(doc):
    seqs = doc.getElementsByTagName('SEQUENCE')
    seq_reps = []
    for seq in seqs:
        algos = seq.getAttribute('algorithm')
        tmp = [seq.getAttribute('input'), algos, seq.getAttribute('output')]
        seq_reps.append(tmp)
    return seq_reps


def dumpSeqDefs(seq_reps):
    unique_seqs = allSeqTypes(seq_reps)
    kkk = unique_seqs.keys()
    # kkk.sort()
    for (ic, type) in enumerate(kkk):
        offset = ''
        c = type.split('->')
        all_names = allSeqTypeInstances(seq_reps, type)
        common_real_names = checkAlgNames(all_names)
        print '#-------------------------------------------------------'
        print '# Sequence type: '+type+' (x '+str(unique_seqs[type])+')'
        print '#-------------------------------------------------------'
        print 'def Seq%d(HltSeq):' % ic
        print '    def __init__(self, seqConfig):'
        print '        (sig_id, pt) = self.extractSigP0(seqConfig)'
        print "        self.inputTE = seqConfig.inputTE"
        print "        self.outputTE = ''"
        print '        self.algorithms = ['
        n = len(c)
        for (ialgo, b) in enumerate(c):
            if b=='': continue
            name = "'%s' + sig_id" % b
            if ialgo == (n-1):
                print "            %s(%s), " % (b, name)
            else:
                print "            %s(), " % (b)
        print '        ]'
        print '\n\n'
    print '# Number of unique sequences: ', len(unique_seqs)
    pass

if __name__=='__main__':
    hltxml = '/space2/tkohno/athena/14.X.0/Trigger/TriggerCommon/TriggerMenuXML/data/HLTconfig_default_14.1.0.xml'
    hltdoc = xml.dom.minidom.parse(hltxml)
    
    seq_reps = readSeqReps(hltdoc)
    print '# Number of sequences: ', len(seq_reps)
    
    # printSeqs(seq_reps)
    # printSeqsPerType(seq_reps)
    dumpSeqDefs(seq_reps)
    
