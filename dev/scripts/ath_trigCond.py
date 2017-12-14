#!/usr/bin/env python
#--------------------------------------------------------------------------
# Extracts luminosity and prescales for each LB for the specified
# triggers and runs.
# *** Only works at CERN (probably needs access to the DB at Tier0)
# Reference: https://twiki.cern.ch/twiki/bin/viewauth/Atlas/CoolOnlineData
#--------------------------------------------------------------------------

import sys
import re
import optparse as op
from PyCool import cool, coral

def parseArgs():
    parser = op.OptionParser()
    parser.add_option('-t', '--trigger', dest='trigger', type='string',
                      action='store', default='', 
                      help='Trigger name (L1, L2 or EF)')
    parser.add_option('-r', '--runs', dest='runs', type='string',
                      action='store', 
                      help='List of runs to check')
    (opts, args) = parser.parse_args()
    return (opts, args)

def getInput(optsargs):
    (opts, args) = optsargs
    trigger = opts.trigger
    runs0 = opts.runs.split(',')
    re0 = re.compile('(\d+)\-(\d+)')
    runs = []
    for r in runs0:
        mg = re0.match(r)
        if mg:
            r1 = int(mg.group(1))
            r2 = int(mg.group(2))
            for a in range(r1, r2+1):
                runs.append(a)
        else:
            runs.append(int(r))
    return (trigger, runs)
    
def connectDB(dbstring):
    dbsvc = cool.DatabaseSvcFactory.databaseService()
    #dbstring = 'COOLONL_TRIGGER/OFLP200'
    #dbstring = 'COOLONL_TRIGGER/COMP200'
    #dbstring = 'COOLOFL_TRIGGER/COMP200'
##     dbstring = "oracle://ATLAS_COOLPROD;schema=ATLAS_COOLONL_TRIGGER"
##     dbstring += ";dbname=COMP200"
##     dbstring += ";user=ATLAS_COOL_READER;password=COOLRED4PRO"
    
    try:
        db = dbsvc.openDatabase(dbstring)
    except Exception, e:
        print 'Problem opening database -> ', e
        sys.exit(-1)
    print 'Opened database "%s"' % dbstring
##     for x in db.listAllNodes():
##         print x
    return db

run = 155697

def getLumiCond(db, run):
    """Return value is a map (LBstart, LBend) -> lumi
    """
    x = {}
    f = db.getFolder('/TRIGGER/LUMI/LBLESTONL')
    objs = f.browseObjects(run<<32, run<<32 | 0xffffffff,
                           cool.ChannelSelection(0))
    while objs.goToNext():
        obj = objs.currentRef()
        r = obj.since() >> 32
        lb0 = obj.since() & 0xffffffff
        lb1 = (obj.until() & 0xffffffff) - 1
        payload = obj.payload()
        lumi = payload['LBAvInstLumi']
        #print 'run %08d (LB %d-%d) lumi=%10.5f' % (r, lb0, lb1, lumi)
        x[(lb0, lb1)] = lumi
    return x

def getL1Config(db, run):
    """Return value is a map 'trigger' -> [(LBstart, LBend, PS), ...]
    """
    x = {}
    m_id2name = {}
    #
    f = db.getFolder('/TRIGGER/LVL1/Menu')
    fps = db.getFolder('/TRIGGER/LVL1/Prescales')
    channsel = cool.ChannelSelection.all()
    #
    objs = f.browseObjects(run<<32, run<<32 | 0xffffffff, channsel)
    while objs.goToNext():
        obj = objs.currentRef()
        r = obj.since() >> 32
        lb0 = obj.since() & 0xffffffff
        lb1 = (obj.until() & 0xffffffff) - 1
        payload = obj.payload()
        id = obj.channelId()
        name = payload['ItemName']
        x[name] = []
        m_id2name[id] = name

    objsps = fps.browseObjects(run<<32, run<<32 | 0xffffffff, channsel)
    while objsps.goToNext():
        obj = objsps.currentRef()
        r = obj.since() >> 32
        lb0 = obj.since() & 0xffffffff
        lb1 = (obj.until() & 0xffffffff) - 1
        id = obj.channelId()
        payload = obj.payload()
        ps = payload['Lvl1Prescale']

        ok = False
        if id in m_id2name.keys():
            name = m_id2name[id]
            x[name].append( (lb0, lb1, ps) )
    return x

def getHLTConfig(db, run):
    """Return value is a map 'trigger' -> [(LBstart, LBend, PS), ...]
    """
    x = {}
    id2name_l2, id2name_ef = {}, {}
    #
    f = db.getFolder('/TRIGGER/HLT/Menu')
    fps = db.getFolder('/TRIGGER/HLT/Prescales')
    channsel = cool.ChannelSelection.all()
    #
    objs = f.browseObjects(run<<32, run<<32 | 0xffffffff, channsel)
    while objs.goToNext():
        obj = objs.currentRef()
        r = obj.since() >> 32
        lb0 = obj.since() & 0xffffffff
        lb1 = (obj.until() & 0xffffffff) - 1
        payload = obj.payload()
        id = obj.channelId()
        name = payload['ChainName']
        counter = payload['ChainCounter']
        level = payload['TriggerLevel']
        lvl = 0
        if level == 'L2': lvl = 0
        elif level == 'EF': lvl = 1
        x[name] = []
        id2name_l2[2*counter+lvl] = name
        
        #print 'Map: %s -> id=%d (counter=%d)' % (name, id, counter)

    #print '%d chains found' % len(id2name)
    n = 0
    objsps = fps.browseObjects(run<<32, run<<32 | 0xffffffff, channsel)
    while objsps.goToNext():
        obj = objsps.currentRef()
        r = obj.since() >> 32
        lb0 = obj.since() & 0xffffffff
        lb1 = (obj.until() & 0xffffffff) - 1
        id = obj.channelId()
        counter = id/2
        level = (id%2) # 0:L2, 1:EF
        payload = obj.payload()
        ps = payload['Prescale']

        ok = False
        name = '???'
        level_from_name = ''
        if id in id2name_l2.keys():
            name = id2name_l2[id]
            x[name].append( (lb0, lb1, ps) )
        #print '[%d] Setting LB for %d, %s, %d' % (n, id, name, obj.objectId())
        n += 1
    #print '%d prescales found' % n
    return x

def prescaleForLB(lb, lbpsv):
    ps = -999
    for lbps in lbpsv:
        if lb>=lbps[0] and (lb<=lbps[1] or lbps[1]==-1):
            ps = lbps[2]
            break
    return ps
def dumpRow(run, lb, lumi, prescales):
    s = '%8d %8d %10.4f' % (run, lb, lumi)
    for p in prescales:
        s += ' %8d' % p
    print s
def dumpTable(run, lb_lumi, triggers, item_lbps):
    nlb = len(lb_lumi)
    keys = item_lbps.keys()
    s = '# Run    LB       LUMI(nb-1) Prescales['
    for t in triggers:
        s += '%s,' % t
    s += ']'
    print s
    for lb in range(1, nlb+1):
        lumi = -999.0
        prescales = [-999]*len(triggers)
        if (lb, lb) in lb_lumi.keys(): lumi = lb_lumi[(lb, lb)]
        for i, t in enumerate(triggers):
            if t in keys: prescales[i] = prescaleForLB(lb, item_lbps[t])
        dumpRow(run, lb, lumi, prescales)

if __name__ == '__main__':
    (trigger, runs) = getInput(parseArgs())
    db_comp = connectDB("oracle://ATLAS_COOLPROD;schema=ATLAS_COOLONL_TRIGGER"
                        + ";dbname=COMP200"
                        + ";user=ATLAS_COOL_READER;password=COOLRED4PRO")
    db_monp = connectDB("oracle://ATLAS_COOLPROD;schema=ATLAS_COOLONL_TRIGGER"
                        + ";dbname=COMP200"
                        + ";user=ATLAS_COOL_READER;password=COOLRED4PRO")

    def dump(name, toLBps, lb_to_lumi):
        nlb = len(lb_to_lumi)
        print 'Item: %s' % name
        print 'LB       PS       LUMI (nb-1)'
        lbpsv = toLBps[name]
        ii = 0
        for lb in range(1, nlb+1):
            lumi = -1.0
            ps = -1000.0
            for lbr in lbpsv:
                if lb >= lbr[0] and lb <= lbr[1]:
                    ps = lbr[2]
                    break
            if (lb, lb) in lb_to_lumi.keys(): lumi = lb_to_lumi[(lb, lb)]
            print '%8d %8d %8.3f' % \
                  (lb, ps, lumi)
                    
        for lbps in lbpsv:
            lb0 = lbps[0]
            lb1 = lbps[1]
            lumi = -1
    def dumpLumi(run, lb_to_lumi):
        keys = map(lambda x: x[0], lb_to_lumi.keys())
        keys.sort()
        for lb in keys:
            print 'LUMI: RUN=%d LB=%d lumi=%5.3f' % (run, lb, lb_to_lumi[(lb, lb)])
        pass
    for run in runs:
        lb_to_lumi = getLumiCond(db_comp, run)
        #dumpLumi(run, lb_to_lumi)
        item_to_lbps = {}
        item_to_lbps.update(getL1Config(db_comp, run))
        item_to_lbps.update(getHLTConfig(db_comp, run))
##         for (k, v) in tmp.iteritems():
##             item_to_lbps[k] = v
        #print 'Run: %08d' % run
        matched = False
        triggers = filter(lambda x: len(x)>0, trigger.split(','))
        dumpTable(run, lb_to_lumi, triggers, item_to_lbps)
##         if len(triggers) == 0: triggers = list(item_to_lbps.keys())
##         for trigger in triggers:
##             if trigger in item_to_lbps.keys():
##                 dump(trigger, item_to_lbps, lb_to_lumi)
##                 matched = True
##     print 'END'
##         print 'print %d triggers' % len(triggers)
##         print triggers
