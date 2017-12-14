#!/usr/bin/env python

import os, sys
import re
import commands
from datetime import datetime
import sqlite3

class JobDefinition:
    def __init__(self):
        self.name = ''
        self.setup_script = ''
        self.executable = ''
        self.input_files = ''
        self.options = {}
        self.output_files = ''
        self.output_destination = ''
        self.working_dir = '.'

    def prepare(self):
        cat 
    def dump(self):
        pass
    
class JobInfo:
    def __init__(self):
        self.type = ''
        self.definition = None
        self.id = -1
        self.state = kNONE

class Pathena:
    pass

class NAFBatch:
    re_qsub = re.compile('Your job (\d+) \(\S+\) has been submitted')
    re_qstat = re.compile('(\d+)\s+([\d.]+)\s+([\w._-]+)\s+([\w._-]+)\s+(\w+)\s+([\d/]+)\s+([\d:]+)')
    
    def __init__(self, db=None):
        self.type = 'NAF'
        self.db = db
        if self.db == None: self.db = JobDB.open()
        pass
    def prepare(self):
        pass

    def db(self):
        return self.db
    
    def submit(self, script):
        cmd = 'qsub %s' % script
        print 'submit NAF job : %s' % cmd
        status, batch_id = self.parse_qsub(commands.getoutput(cmd))
        if status != 'SUCCESS':
            print 'Error while submitting the script %s to NAF' % script
            return
        #
        logfile = '%s.o%07d' % (script, batch_id)
        print 'logfile: %s' % logfile
        #
        name = os.path.basename(script)
        name = name[0:name.rfind('.')]
        rows = self.db.findJob(name, script)
        id = 0
        if len(rows) == 0:
            self.db.insertJob(name, script)
            id = self.db.lastrowid()
        else:
            id = rows[0][0]
        if id > 0:
            #rows = self.findJobInfoWithJobId(id)
            self.db.insertJobInfo(self.type, id, batch_id, logfile,
                                  os.getenv('HOST'), os.getcwd())
        return
    
    def update(self):
        user = os.getenv('USER')
        if user == '': user = 'tkohno'
        cmd = 'qstat -u %s' % user
        status, jobs = self.parse_qstat(commands.getoutput(cmd))
        if status != 'SUCCESS':
            print 'Error while checking the status with qstat'
        rows = self.db.findJobInfoWithStatus('SUBMITTED')
        rows.extend(self.db.findJobInfoWithStatus('RUNNING'))
        rows.extend(self.db.findJobInfoWithStatus('WAITING'))
        #
        job_status_map = {}
        for j in jobs:
            job_status_map[j[0]] = j[1]
        for r in rows:
            db_id = r[0]
            batch_id = r[1]
            db_status = r[2]
            if batch_id in job_status_map.keys():
                db_new = ''
                status = job_status_map[batch_id]
                if status == 'r': db_new = 'RUNNING'
                if status.find('E')>=0: db_new = 'ERROR'
                if status.find('w')>=0: db_new = 'WAITING'
            else:
                db_new = 'FINISHED'
            if (db_new == 'RUNNING' and db_status != 'RUNNING') or \
               (db_new == 'WAITING' and db_status == 'SUBMITTED') or \
               (db_new == 'ERROR' and db_status != 'ERROR') or \
               (db_new == 'FINISHED' and db_status != 'FINISHED'):
                self.db.updateJobInfo(db_id, db_new)
        return
    
    def parse_qsub(self, stream):
        """Look for a line like
        Your job 2262186 ("run.3.sh") has been submitted"""
        status, batch_id = 'UNKNOWN', 0
        for s in stream.split(os.linesep):
            mg = NAFBatch.re_qsub.match(s)
            if mg:
                status = 'SUCCESS'
                batch_id = int(mg.group(1))
        return (status, batch_id)

    def parse_qstat(self, stream):
        """Look for a line like
        2262186 0.50135 run.3.sh   tkohno       Eqw   10/12/2010 13:53:53"""
        status, job_status = 'UNKNOWN', []
        for s in stream.split(os.linesep):
            mg = NAFBatch.re_qstat.match(s)
            #print 's=%s, mg=%s' % (s, mg!=None)
            if mg:
                job_status.append( (int(mg.group(1)), mg.group(5)))
        status = 'SUCCESS'
        return (status, job_status)
    pass


class JobDB:
    _dbs = {}
    def open(dbname = ''):
        if dbname == '': dbname = '%s/jobmgr.db' % os.getenv('HOME')
        if dbname in JobDB._dbs.keys():
            return JobDB._dbs[dbname]
        elif os.path.exists(dbname):
            db = JobDB(dbname)
            JobDB._dbs[dbname] = db
            return db
        else:
            schema = '%s/share/jobmgr_schema.sql' % os.getenv('TK_ROOT')
            cmd = 'sqlite3 -init %s %s' % (schema, dbname)
            os.system(cmd)
            db = JobDB(dbname)
            JobDB._dbs[dbname] = db
            return db
    open = staticmethod(open)
    
    def __init__(self, database):
        print 'Opening sqlite database: %s' % database
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def dump(self):
        rows = self.cursor.execute('SELECT * FROM job_definition')
        for r in rows.fetchall():
            print r
        rows = self.cursor.execute('SELECT * FROM job_info')
        for r in rows.fetchall():
            print r

    def findJob(self, name, script):
        stmt = 'SELECT id FROM job_definition WHERE name=? AND script=?'
        rows = self.cursor.execute(stmt, (name, script,))
        return rows.fetchall()
    
    def findJobInfoWithStatus(self, status, reverse_logic=False):
        stmt = "SELECT id,batch_id,status FROM job_info WHERE status=?"
        bikkuri = ''
        if reverse_logic:
            stmt = "SELECT id,batch_id,status FROM job_info WHERE NOT status=?"
            bikkuri = '!'
        rows = self.cursor.execute(stmt, (status,))
        return rows.fetchall()

    def findJobInfoWithJobId(self, id):
        stmt = 'SELECT id,batch_id,status FROM job_info WHERE job_id=?'
        rows = self.cursor.execute(stmt, (id,))
        return rows.fetchall()
        
    def insertJob(self, name, script):
        stmt = 'INSERT INTO job_definition VALUES (?,?,?)'
        self.cursor.execute(stmt, (None, name, script))
        self.connection.commit()
        pass

    def insertJobInfo(self, type, job_id, batch_id, logfile, host, location):
        dt = datetime.now()
        t = dt.strftime('%Y-%m-%d %H:%M:%S')
        stmt = 'INSERT INTO job_info VALUES (?,?,?,?,?,?,?,?,?,?)'
        self.cursor.execute(stmt, (None, type, job_id, batch_id, logfile,
                                   host, location, t, t, 'SUBMITTED'))
        self.connection.commit()
        pass
    
    def updateJobInfo(self, id, status):
        dt = datetime.now()
        t = dt.strftime('%Y-%m-%d %H:%M:%S')
        stmt = "UPDATE job_info SET last_updated=?,status=?"
        stmt += " WHERE id=?"
        #print stmt
        self.cursor.execute(stmt, (t, status, id))
        self.connection.commit()
        pass

    def lastrowid(self):
        return self.cursor.lastrowid

    pass

def testDB():
    db = JobDB('ex.sqlite')
    #db.insertJobInfo('NAF', 1, 13533, 'log.txt', 'lxplus', '/tmp/tkohno')
    #rowid = db.cursor.lastrowid
    #db.listJobs()
    #print 'Updating the newest row ', rowid
    #rows = db.updateJobInfo(rowid, 'FINISHED')
    #print rows
    db.listJobs()
    db.findJobs('SUBMITTED')
    db.findJobs('FINISHED')
    db.findJobs('SUBMITTED', True)

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--qsub', dest='do_qsub',
                      action='store_true', default=False,
                      help='Submit jobs')
    parser.add_option('--dumpDB', dest='dumpDB',
                     action='store_true', default=False,
                     help='Dump all entries in the database')
    parser.add_option('-u', '--update', dest='update',
                     action='store_true', default=False,
                     help='Update job status in the database')

    (options, args) = parser.parse_args()
    print options

    db = JobDB.open()
    batch = NAFBatch(db)
    
    if options.update: batch.update()
    
    if options.do_qsub:
        print 'Submit %d scripts' % len(args)
        for script in args:
            batch.submit(script)

    if options.dumpDB:
        db.dump()
    sys.exit(0)
        

