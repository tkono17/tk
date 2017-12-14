#!/usr/bin/env python

import sys
from PyCool import cool, coral
import optparse as op

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
    runs = map(lambda x: int(x), opts.runs.split(','))
    return (trigger, runs)
    
def connectDB():
    dbsvc = cool.DatabaseSvcFactory.databaseService()
    dbstring = 'COOLONL_TRIGGER/OFLP200'
    dbstring = 'COOLONL_TRIGGER/COMP200'
    #dbstring = 'COOLOFL_TRIGGER/COMP200'
    
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

def getTrigCond(db, run, folderNames):
    """Return value is a map 'trigger' -> [(LBstart, LBend, PS), ...]
    """
    print 'getTrigCond'
    x = {}
    MenuFolder = folderNames[0]
    PrescaleFolder = folderNames[1]
    PrescalePayload = folderNames[2]
    TriggerName = folderNames[3]
    #
    f = db.getFolder(MenuFolder)
    fps = db.getFolder(PrescaleFolder)
    channsel = cool.ChannelSelection.all()
    #
    objsps = fps.browseObjects(run<<32, run<<32 | 0xffffffff, channsel)
    
    runctpid_to_lbps = {}

    while objsps.goToNext():
        obj = objsps.currentRef()
        r = obj.since() >> 32
        lb0 = obj.since() & 0xffffffff
        lb1 = (obj.until() & 0xffffffff) - 1
        ctpid = obj.channelId()
        payload = obj.payload()
        ps = payload[PrescalePayload]

        if (r, ctpid) in runctpid_to_lbps.keys():
            runctpid_to_lbps[(r, ctpid)].append( (lb0, lb1, int(ps)))
        else:
            runctpid_to_lbps[(r, ctpid)] = [(lb0, lb1, ps)]

    # Get the item name from the CTPID
    objs = f.browseObjects(run<<32, run<<32 | 0xffffffff, channsel)
    y = {}
    print 'OBJS'
    print objs
    print dir(objs)
    while objs.goToNext():
        obj = objs.currentRef()
        r = obj.since() >> 32
        lb0 = obj.since() & 0xffffffff
        lb1 = (obj.until() & 0xffffffff) - 1
        ctpid = obj.channelId()
        payload = obj.payload()
        item = payload[TriggerName]
        print 'Trigger %s id=%d' % (item, ctpid)
        if (run, ctpid) in runctpid_to_lbps.keys():
            y[item] = runctpid_to_lbps[(run, ctpid)]
    print 'DONE'
    return y
    

if __name__ == '__main__':
    (trigger, runs) = getInput(parseArgs())
    db = connectDB()
    folderNames = [
        '/TRIGGER/HLT/Menu', 
        '/TRIGGER/HLT/Prescales', 
        'Prescale',
        'ChainName',
        
        '/TRIGGER/LVL1/Menu', 
        '/TRIGGER/LVL1/Prescales', 
        'Lvl1Prescale',
        'ItemName', 
        ]
    
    def dump(name, toLBps):
        print '  Item %s' % name
        lbpsv = toLBps[name]
        for lbps in lbpsv:
            print '    (%4d, %4d) PS=%d' % lbps
    for run in runs:
        item_to_lbps = getTrigCond(db, run, folderNames)
        print 'Run %08d' % run
        if trigger in item_to_lbps.keys():
            dump(trigger, item_to_lbps)
        else:
            kk = list(item_to_lbps.keys())
            kk.sort()
            for t in kk:
                dump(t, item_to_lbps)
