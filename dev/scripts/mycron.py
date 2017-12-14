#!/usr/bin/env python
#--------------------------------------------------------------------------
# Launch scheduled jobs at login time
#-------------------------------------
# - Reads the configuration file specified by the environment variable
#   TK_CRON_CONF (e.g. $HOME/work/cron.conf)
# - The format of the configuration file
#   [<host>:]<domain> <interval> <command>
#   - <interval> := \d+  : Number of times the script is called in a sequence
#                 | \d+s : Every X seconds
#                 | \d+m : Every X minutes
#                 | \d+h : Every X hours
#                 | \d+d : Every X days
#                 | S    : Command needed as a setup (execute this first)
# - Start it on logon if there is no other instance of this script running
#   It checks the existence of the file ${TK_CRON_CONF}.lock which contains
#   the host and the last accessed date of this file
#--------------------------------------------------------------------------
import os, sys
import subprocess
import re
import datetime, time
import socket
import optparse
import logging
import subprocess
import atexit

logging.basicConfig(level=logging.DEBUG,
                    #format='%(asctime)s %(levelname)s %(message)s',
                    format='mycron.py:  %(levelname)s  %(message)s',
                    filename='', 
                    filemode='w')
log = logging.getLogger('mycron.py')
log.setLevel(logging.INFO)

def readConf(conf):
    x = []
    re0 = re.compile('(\S+)\s+(\S+)')
    re1 = re.compile('(\d+)(m|h|d){0,1}')
    if os.path.exists(conf):
        f = open(conf, 'r')
        for line in f.readlines():
            if len(line)==0 or line[0]=='#': continue
            else: line = line[:-1]
            mg = re0.search(line)
            if mg:
                hostdomain = mg.group(1)
                interval = mg.group(2)
                cmd = line[len(mg.group(0)):].strip()
                if cmd.startswith('"') and cmd.endswith('"'):
                    cmd = cmd.strip('"')
                if cmd.startswith("'") and cmd.endswith("'"):
                    cmd = cmd.strip("'")
                hostdomain = hostdomain.replace('.', '\.').replace('*', '.*')
                x.append( (hostdomain, interval, cmd))
##                 print 'hostdomain: %s' % hostdomain
##                 print 'interval  : %s' % interval
##                 print 'command   : %s' % cmd
            pass
    else:
        print 'File not there: '
        pass
    return x

def read_lock(fname):
    m = {}
    if not os.path.exists(fname):
        update_lock(fname, '', 'STOPPED')
    f = open(fname, 'r')
    re0 = re.compile('(\w+):\s*([\w/:_.\s]+)')
    for line in f.readlines():
        if len(line)>0: line = line[:-1]
        mg = re0.match(line)
        if mg:
            m[mg.group(1)] = mg.group(2)
    return m

def is_mine(m):
    s = False
    if m.has_key('User') and m.has_key('tty') and m.has_key('Host'):
        p = subprocess.Popen('tty', stdout=subprocess.PIPE)
        tty = p.stdout.read().rstrip(os.linesep)
        s = m['User'] == os.getlogin() and m['tty'] == tty and \
            m['Host'] == socket.gethostname()
    return s

def remove_lock(fname):
    if os.path.exists(fname):
        os.remove(fname)
        log.info('Removed %s' % lock)

def update_lock(fname, conf, status):
    m = {}
    if os.path.exists(fname):
        m = read_lock(fname)
        if m['Status'] == 'LOCKED' and not is_mine(m):
            return
    now = datetime.datetime.now()
    tmp = fname+'.writing'
    if os.path.exists(tmp): os.remove(tmp)
    p = subprocess.Popen('tty', stdout=subprocess.PIPE)
    tty = p.stdout.read().rstrip(os.linesep)
    f = open(tmp, 'w')
    f.write('User:   %s\n' % os.getlogin())
    f.write('tty:    %s\n' % tty)
    f.write('Host:   %s\n' % socket.gethostname())
    f.write('Time:   %s\n' % now.strftime('%Y/%m/%d %H:%M:%S'))
    f.write('Conf:   %s\n' % conf)
    f.write('Status: %s\n' % status)
    f.close()
    if os.path.exists(fname): os.remove(fname)
    os.rename(tmp, fname)
    log.debug('Updated %s' % lock)
    pass

def parse_args():
    """Arguments := start | stop | status| owns """
    op = optparse.OptionParser()
    op.add_option('-s', '--setup', dest='setup',
                  action='store_true', default=False, 
                  help='Only run the setup commands')
    op.add_option('-m', '--main', dest='main',
                  action='store_true', default=False, 
                  help='Only run the main commands')
    op.add_option('-f', '--force', dest='force',
                  action='store_true', default=False, 
                  help='Force action')
    op.add_option('-l', '--output-level', dest='output_level',
                  action='store', default='INFO', 
                  help='Output level (DEBUG=10|INFO=20|ERROR=40|FATAL=50)')
    op.add_option('-c', '--cron-conf', dest='cron_conf',
                  action='store', default='',
                  help='Specify the cron.conf file (default=$TK_CRON_CONF)')
    return op.parse_args()

class JobSchedule:
    re1 = re.compile('(\d+)(s|m|h|d){0,1}')
    def __init__(self, id, cmd, interval):
        self.id = id
        self.command = cmd
        self.last_call_time = None
        self.next_call_time = datetime.datetime.now()
        self.remaining_number_of_calls = 0
        self.interval = None
        mg = JobSchedule.re1.match(interval)
        if mg:
            # Set the interval in units of seconds
            number = int(mg.group(1))
            unit = mg.group(2)
            log.debug('Interval string matches: %s' % str(mg.groups()))
            if unit == None: 
                # number of calls instead of the interval
                self.remaining_number_of_calls = int(number)
            elif unit == 's':
                self.interval = datetime.timedelta(seconds=int(number))
            elif unit == 'm':
                self.interval = datetime.timedelta(minutes=int(number))
            elif unit == 'h':
                self.interval = datetime.timedelta(hours=int(number))
            elif unit == 'd':
                self.interval = datetime.timedelta(days=int(number))
        elif interval == 'S':
            self.number = 1
    def run(self):
        now = datetime.datetime.now()
        log.info('Run cmd=%s (%s)' % (self.command, now.ctime() ) )
        cmd = self.command
        p = subprocess.call(cmd, shell=True)
        #stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        now = datetime.datetime.now()
        log.debug('Interval = %s' % str(self.interval))
        if self.interval != None:
            self.last_call_time = now
            self.next_call_time = now + self.interval
            log.debug('Next call time %s (after %d seconds)' % \
                      (self.next_call_time.ctime(), self.interval.seconds))
        elif self.remaining_number_of_calls > 0:
            self.last_call_time = now
            self.next_call_time = now
            self.remaining_number_of_calls -= 1
            if self.remaining_number_of_calls == 0:
                self.next_call_time = None
        pass

class JobSchedular:
    def __init__(self, rules, last_update_time=None):
        self.rules = rules
        self.last_update = last_update_time
        self.scheduled_jobs = []
        self.createJobs()
    def createJobs(self):
        for i, r in enumerate(self.rules):
            j = JobSchedule(i, r[2], r[1])
            if self.last_update: j.last_call_time = self.last_update
            self.scheduled_jobs.append(j)
    def update(self):
        t = None # the closest next time from now to call some job
        n = 0
        now = datetime.datetime.now()
        log.info('Updating schedule for %d jobs [%s]' % \
                 (len(self.scheduled_jobs), now.ctime()))
        for j in self.scheduled_jobs:
            #print dir(j)
            log.debug('Call time %s' % j.next_call_time.ctime())
            if j.next_call_time == None:
                log.debug('Job not scheduled anymore')
                continue
            now = datetime.datetime.now()
            if j.next_call_time < now:
                log.debug('Calling job')
                j.run()
            else:
                log.debug('Job scheduled later at %s' % \
                          j.next_call_time.ctime())
            if j.next_call_time != None:
                n += 1
                if t == None: t = j.next_call_time
                elif j.next_call_time < t:
                    t = j.next_call_time
        sleep_time = 1
        if t == None:
            sleep_time = -1
        else:
            time.sleep(1)
            now = datetime.datetime.now()
            dt = t - now
            log.debug('Next time %s <-> now %s' % (t.ctime(), now.ctime()))
            if dt < datetime.timedelta(0, 0, 0): sleep_time = 1
            else: sleep_time = dt.seconds + 1
        log.info('Scheduling %d jobs in %d seconds' % (n, sleep_time))
        return sleep_time

if __name__ == '__main__':
    options, args = parse_args()
    conf, rules = '', []
    lock = ''
    arg = ''
    #print args
    if options.output_level == 'DEBUG': log.setLevel(logging.DEBUG)

    if options.cron_conf != '': os.environ['TK_CRON_CONF'] = options.cron_conf
    if os.environ.has_key('TK_CRON_CONF'):
        conf = os.environ['TK_CRON_CONF']
        lock = conf.replace('.conf', '.lock')
        rules = readConf(conf)
        log.debug('Lock file: %s' % lock)
    #
    atexit.register(update_lock, lock, conf, 'STOPPED')
    #
    host = socket.gethostname()
    if len(args)>0: arg = args[0]
    rules1 = []
    for r in rules:
        if re.match(r[0], host):
            rules1.append(r)
    if arg == 'start':
        log.info('Starting my cron (%s)' % conf)
        log.info('%d rules defined -> %d on %s' % \
                     (len(rules), len(rules1), host ) )
        #
        last_update_time = None
        m = read_lock(lock)
        mg = re.search('(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)', m['Time'])
        if mg:
            last_update_time = datetime.datetime(int(mg.group(1)), 
                                                 int(mg.group(2)), 
                                                 int(mg.group(3)), 
                                                 int(mg.group(4)), 
                                                 int(mg.group(5)), 
                                                 int(mg.group(6)))
            log.info('Last updated at %s' % last_update_time.ctime())
        locked = False
        if m['Status'] == 'LOCKED':
            locked = True
            log.warning('%s is LOCKED by %s/%s (last update:%s)' % \
                            (conf, m['Host'], m['tty'], m['Time']) )
        rules_setup, rules_main = [], []
        for r in rules1:
            if r[1] == 'S': rules_setup.append(r)
            else: rules_main.append(r)
        if options.setup and not locked:
            js = JobSchedular(rules_setup, last_update_time)
        #elif (options.main or len(rules_setup) == 0) and not locked:
        elif (options.main) and not locked:
            log.info('Start scheduling jobs')
            update_lock(lock, conf, 'LOCKED')
            js = JobSchedular(rules_main, last_update_time)
            sleep_time = 1
            while sleep_time > 0:
                time.sleep(sleep_time)
                sleep_time = js.update()
            log.info('Finished running all scheduled jobs')
            update_lock(lock, conf, 'STOPPED')
        elif not (options.main or options.setup) and not locked:
            log.info('%d setup commands are necessary' % len(rules_setup))
            base = os.path.basename(conf).replace('.conf', '')
            s = 'start_%s.sh' % base
            if os.path.exists(s): os.remove(s)
            f = open(s, 'w')
            ts = '-'
            if last_update_time: ts = last_update_time.ctime()
            f.write('#!/usr/bin/env zsh\n')
            f.write('# Last update: %s on %s\n' % (ts, m['Host']))
            f.write('# Setup commands\n')
            for r in rules_setup:
                f.write('%s\n' % r[2])
            f.write('\n# Main jobs for scheduling\n')
            for r in rules_main:
                f.write('# (%s) %s\n' % (r[1], r[2]))
            f.write('mycron.py -m --cron-conf=%s start\n' % conf)
            log.info('Run ./%s to start cron jobs' % s)
            os.chmod(s, 0755)
            ret = subprocess.call('cat %s' % s, shell=True)
    elif arg == 'status':
        if os.path.exists(lock):
            log.info('Starting my cron (%s)' % conf)
            log.info('%d rules defined -> %d on %s' % \
                     (len(rules), len(rules1), host ) )
            m = read_lock(lock)
            p = subprocess.Popen('tty', stdout=subprocess.PIPE)
            tty = p.stdout.read().rstrip(os.linesep)
            print '#--------------------------------'
            print 'User:   %s' % (m['User'])
            print 'Host:   %s' % (m['Host'])
            print 'tty:    %s' % (m['tty'])
            print 'Conf:   %s' % (m['Conf'])
            print 'Status: %s' % (m['Status'])
            print 'Time:   %s' % (m['Time'])
            print '#--------------------------------'
        else:
            log.warning('No lock file %s exists' % lock)
    elif arg == 'stop':
        if os.path.exists(lock):
            m = read_lock(lock)
            p = subprocess.Popen('tty', stdout=subprocess.PIPE)
            tty = p.stdout.read().rstrip(os.linesep)
            log.debug('User: %s <-> %s' % (m['User'], os.getlogin()))
            log.debug('Host: %s <-> %s' % (m['Host'], socket.gethostname()))
            log.debug('tty: %s <-> %s' % (m['tty'], tty))
            if options.force or is_mine(m):
                update_lock(lock, conf, 'STOPPED')
    elif arg == 'clear':
        if os.path.exists(lock): remove_lock(lock)        

