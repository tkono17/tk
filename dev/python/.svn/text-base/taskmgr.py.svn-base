#!/usr/bin/env python
#---------------------------------------------------------------------
# taskmgr.py
#-----------
# Task manager for running multiple jobs
# Task is defined as producing certain outputs from inputs
#---------------------------------------------------------------------
import os, sys
import re
import time
import optparse
import cPickle
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s',
                    filename='', #filename='/tmp/myapp.log',
                    filemode='w')
log = logging.getLogger('taskmgr.py')
log.setLevel(logging.INFO)

#---------------------------------------------------------------------
# Classes for the task definition
#---------------------------------------------------------------------
class Status:
    kDefined = 'DEFINED'
    kPrepared = 'PREPARED'
    kRunning = 'RUNNING'
    kWaiting = 'WAITING'
    kFinished = 'FINISHED'
    kFailed = 'FAILED'
    kCancelled = 'CANCELLED'
    kCompleted = 'COMPLETED'

class TaskDefinition:
    def __init__(self, name):
        self.name = name
        self.executable = 'echo'
        self.inputFiles = []
        self.outputFiles = []
    def __str__(self):
        s = 'name: %s\n' % self.name
        return s
    pass

#---------------------------------------------------------------------
# Classes for the running task (input -> output)
#---------------------------------------------------------------------

class TaskAction:
    def __init__(self, name, cmd):
        self.name = name
        self.cmd = cmd
        self.out = ''
        self.err = ''
        self.logs = []
    def __str__(self):
        s = '  %-8s => "%s"\n' % (self.name, self.cmd)
        if self.out != '':
            s += '              out=%s\n' % self.out
        if self.err != '':
            s += '              err=%s\n' % self.err
        return s
    pass

# Possible task action names
kPrepare = 'PREPARE'
kRun = 'RUN'
kUpdate = 'UPDATE'
kRerun = 'RERUN'
kPostrun = 'POSTRUN'

class TaskTransition:
    def __init__(self, out_state, action, in_states):
        self.action = action
        self.out_state = out_state
        if type(in_states) == type([]):
            self.in_states = list(in_states)
        else:
            self.in_states = [in_states]

class TaskTransitionRules:
    """ inputs - (action) -> output"""
    def __init__(self):
        self.rules = [
            # prepare
            TaskTransition(Status.kPrepared, 'PREPARE', Status.kDefined),
            # run
            TaskTransition(Status.kWaiting, 'RUN', Status.kPrepared),
            # update
            TaskTransition(Status.kRunning, 'UPDATE', Status.kWaiting), 
            TaskTransition(Status.kFinished, 'UPDATE', \
                           [Status.kRunning, Status.kWaiting]), 
            TaskTransition(Status.kFailed, 'UPDATE', \
                           [Status.kRunning, Status.kWaiting]), 
            TaskTransition(Status.kCancelled, 'UPDATE', \
                           [Status.kRunning, Status.kWaiting]), 
            TaskTransition(Status.kWaiting, 'UPDATE', \
                           [Status.kRunning, Status.kFailed, Status.kCancelled]), 
            # rerun
            TaskTransition(Status.kWaiting, 'RERUN', 
                           [Status.kFailed, Status.kCancelled]),
            # postrun
            TaskTransition(Status.kCompleted, 'POSTRUN', \
                           Status.kFinished), 
            ]
    def getRulesForAction(self, action):
        return filter(lambda x: x.action==action, self.rules)
    def getInStatesForAction(self, action):
        rules = self.getRulesForAction(action)
        states = []
        for r in rules:
            #log.info('Checking in states for %s' % action)
            for s in r.in_states:
                #print 's = %s' % s
                if s not in states: states.append(s)
        return states
    def getOutStatesForAction(self, action, input):
        rules = self.getRulesForAction(action)
        states = []
        for r in rules:
            if input not in r.in_states: continue
            if r.out_state not in states: states.append(r.out_state)
        return states

class Task:
    def __init__(self, taskdef):
        self.taskDefinition = taskdef
        self.status = Status.kDefined
        # Secondary data
        self.action_prepare = TaskAction('prepare', 'echo prepare')
        self.action_run = TaskAction('run', 'echo run')
        self.action_update = TaskAction('update', 'echo update')
        self.action_rerun = TaskAction('rerun', 'echo rerun')
        self.action_postrun = TaskAction('postrun', 'echo postrun')
        # Temporary data
        self.do_echo = False
        #self.transition_rules = None
    def action(self, task_action, transition_rules=None):
        funcname = task_action.lower()
        # print 'status = %s' % self.status
        inputs, outputs = [], []
        if transition_rules:
            # check if the action is allowed on the current state
            inputs = transition_rules.getInStatesForAction(task_action)
            outputs = transition_rules.getOutStatesForAction(task_action,
                                                             self.status)
            if len(inputs) > 0 and self.status not in inputs:
                log.debug('Action %s not defined for current state %s' % \
                            (task_action, self.status))
                log.debug('inputs = %s' % str(inputs))
                log.debug('outputs = %s' % str(outputs))
                return False
        func, state = None, False
        if hasattr(self, funcname): func = getattr(self, funcname)
        if func:
            log.info('Action %s on task %s (status=%s)' % \
                     (task_action, self.taskDefinition.name, self.status))
            state = func()
        else:
            log.warning('Do not know which function to call for action: %s' % \
                        task_action)
            return False
        if state:
            if transition_rules:
                if len(inputs)==0 or state in outputs:
                    self.status = state
                elif self.status != state:
                    log.warning('State transition not allowed %s: %s-(%s)->%s' %  \
                                (self.taskDefinition.name,
                                 self.status, task_action, state))
                    return False
            else:
                self.status = state
        return True
    def prepare(self):
        return False
    def run(self):
        return False
    def rerun(self):
        return False
    def postrun(self):
        return False
    def execCmd(self, cmd):
        if self.do_echo:
            log.info('Just echo the given command')
            cmd = 'echo %s' % cmd
        log.debug('Executing command %s ...' % cmd)
        out, err = None, None
        try:
            p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            (out, err) = p.communicate()
        except OSError:
            log.warning('OSError while executing command %s' % cmd)
        return (out, err)
    def saveToFile(self, fname, msg):
        try:
            f = open(fname, 'w')
            if msg:
                f.write(msg)
            f.close()
        except IOError: # as detail:
            log.warning('IOError while writing to file %s' % fname)
            #print detail
    def dump(self):
        pass
    def printDetails(self):
        pass
    def printSummary(self):
        s = '%-40s: %s' % (self.taskDefinition.name, self.status)
        print s
    def __str__(self):
        s = 'TaskDefinition:\n'
        s += '  %s' % str(self.taskDefinition)
        s += 'Status: %s\n' % self.status
        s += 'Commands:\n'
        s += str(self.action_prepare)
        s += str(self.action_run)
        s += str(self.action_update)
        s += str(self.action_rerun)
        s += str(self.action_postrun)
        return s
    pass

class LocalTask(Task):
    def __init__(self, jobdef):
        super(LocalTask, self).__init__(jobdef)
    def prepare(self):
        return False
    def run(self):
        return False
    def rerun(self):
        return False
    def postrun(self):
        return False
    def dump(self):
        pass
    def printDetails(self):
        pass
    pass

#---------------------------------------------------------------------
# Main task manager class
#---------------------------------------------------------------------
class TaskMgr:
    def __init__(self, name='', filename='taskmgr.pickle'):
        self.name = name
        self.storageFileName = filename
        self.tasks = []
        # Temporary data
        self.options = None
        self.transition_rules = TaskTransitionRules()
        pass
    def addTask(self, task):
        if task.taskDefinition == None:
            log.warning('Tried to add a task with no job definition info')
        else:
            names = map(lambda x: x.taskDefinition.name, self.tasks)
            nm = task.taskDefinition.name
            if nm in names:
                log.warning('Task with name=%s already exists' % nm)
            else:
                task.transition_rules = self.transition_rules
                self.tasks.append(task)
        return self
    def findTask(self, name):
        for t in self.tasks:
            if t.taskDefinition.name == name:
                return t
        return None
    def deleteTask(self, name):
        v = []
        n0 = len(self.tasks)
        for t in self.tasks:
            if t.taskDefinition.name != name:
                v.append(t)
            else:
                log.info('Removing task %s' % name)
        if len(v) == (n0-1):
            self.tasks = v
    def isEnabled(self, task_action):
        s = task_action.lower()
        actionlist = self.options.actions.split(',')
        if actionlist.count(s) > 0:
            return True
        else:
            return False
    def action(self, task_action, names=[]):
        funcname = task_action.lower()
        ret = False
        if funcname == '': return ret
        for t in self.tasks:
            if len(names)>0 and t.taskDefinition.name not in names: continue
            if self.options.quiet_run: t.do_echo = True
            else: t.do_echo = False
##             if t.taskDefinition.name == '2011.periodM':
##                 t.addJobSet(8772, 8774, 0, '?')
##                 t.addJobSet(8772, 8775, 0, '?')
##                 t.addJobSet(8772, 8776, 0, '?')
##                 t.addJobSet(8772, 8777, 0, '?')
##                 t.addJobSet(8772, 8778, 0, '?')
##                 t.addJobSet(8772, 8779, 0, '?')
##             #    t.status = Status.kWaiting
            if task_action == kRerun and self.options.force_rerun and \
                   t.status in (Status.kWaiting, Status.kRunning):
                log.info('State modified to force rerun: %s->%s' %
                         (t.status, Status.kFailed))
                t.status = Status.kFailed
            ret = t.action(task_action, self.transition_rules)
            self.save()
        return ret
        
    def takeBestActions(self):
        log.info('Take an appropriate action for each task, updating status.')
        mgr.action(kUpdate)
        log.info('Processing tasks ...')
        for t in self.tasks:
            if self.options.quiet_run: t.do_echo = True
            else: t.do_echo = False
            status0 = t.status
            act = ''
            if t.status == Status.kDefined: act = kPrepare
            elif t.status == Status.kPrepared: act = kRun
            elif t.status in (Status.kCancelled, Status.kFailed): act = kRerun
            if act != '':
                ret = t.action(act, self.transition_rules)
                log.info('Task %s %s-(%s)->%s' % \
                         (t.taskDefinition.name, status0, act, t.status))
        time.sleep(60)
        self.action(kUpdate)
        self.action('summary')
        if self.status() == Status.kFinished:
            os.system('mail -s "FINISHED: %s"' % (self.storageFileName))
        pass
    def status(self):
        """Need fix"""
        s = Status.kFinished
        for t in self.tasks:
            if t.status != Status.kFinished: s = '???'
        return s
    def dump(self, names=[]):
        log.info('TaskMgr file: %s' % self.storageFileName)
        log.info('%d tasks defined' % len(self.tasks))
        for t in self.tasks:
            if len(names)>0 and t.taskDefinition.name not in names: continue
            print '#-----------------------------------------------------'
            print t
            print '#-----------------------------------------------------'
    def printSummary(self):
        log.info('TaskMgr file: %s' % self.storageFileName)
        print '%d tasks defined' % len(self.tasks)
        for t in self.tasks:
            t.printSummary()
    def load(self):
        fname = self.storageFileName
        if fname.endswith('.pickle'):
            f = open(fname, 'rb')
            obj = None
            try:
                objs = cPickle.load(f)
                if len(objs)>0: self.name = objs[0]
                if len(objs)>1: self.storageFileName = objs[1]
                if len(objs)>2: self.tasks = objs[2]
            except EOFError:
                pass
            f.close()
        pass
    def save(self):
        fname = self.storageFileName
        if fname.endswith('.pickle'):
            f = open(fname, 'wb')
            objs = (self.name, self.storageFileName, self.tasks)
            cPickle.dump(objs, f)
            f.close()
    pass

#---------------------------------------------------------------------
# Main program
#---------------------------------------------------------------------
def parse_options():
    op = optparse.OptionParser()
    # Basic options
    op.add_option('--name', dest='name',
                  action='store', default='',
                  help='Name of the list of tasks to manage')
    op.add_option('-f', '--storage-file', dest='storage_file',
                  action='store', default='',
                  help='Storage file for storage (.pickle and later .xml)')
    op.add_option('-d', '--delete-tasks', dest='delete_tasks', 
                  action='store_true', default=False,
                  help='Delete tasks. Task names should be specified by -n <name1,name2>')
    op.add_option('-n', '--task-names', dest='task_names',
                  action='store', default='',
                  help='Task name to take some actions')
    op.add_option('-s', '--set-status', dest='set_status',
                  action='store', default='',
                  help='Set status to the given value')
    op.add_option('--task-type', dest='task_type', 
                  action='store', default='', 
                  help='Task type (only pathena available for now)')
    op.add_option('--process-tasks', dest='process_tasks',
                  action='store_true', default=False,
                  help='Take an appropriate action for each task')

    # pathena options
    op.add_option('--dataset-alias-file', dest='dataset_alias_file', 
                  action='store', default='',
                  help='Dataset alias definition file')
    op.add_option('--jobOptions', dest='job_options', 
                  action='store', default='',
                  help='Job options file')
    op.add_option('-v', '--version', dest='version',
                  action='store', default='v1',
                  help='Version number to be appended for pathena output DS')
    
    # control options
    op.add_option('-a', '--actions', dest='actions',
                  action='store', default='', 
                  help='Comma separated list of actions (prepare,run,update,rerun,dump,parse_run,summary)')
    op.add_option('--force-rerun', dest='force_rerun',
                  action='store_true', default=False,
                  help='Force rerun. Overwrite the task status as failed')
    op.add_option('-l', '--log-level', dest='log_level', 
                  action='store', default='INFO',
                  help='Log level (DEBUG|INFO|WARNING|ERROR)')
    op.add_option('-q', '--quiet-run', dest='quiet_run',
                  action='store_true', default=False, 
                  help='Quiet run. All commands will be replaced by echo')
    op.add_option('--show-examples', dest='show_examples', 
                  action='store_true', default=False,
                  help='Show examples')
    op.add_option('--create-submit-script', dest='create_submit_script',
                  action='store', default='',
                  help='Create the submit script')
                  
    return op.parse_args()

def getDatasets(dataset_alias_file):
    ds = []
    if os.path.exists(dataset_alias_file):
        execfile(dataset_alias_file)
        ds = locals()['datasets']
    return ds

def showExamples():
    print """Some examples:
o Standard pathena job management
  0) Produce the original submission script
     taskmgr.py --create-submit-script=submit_script.sh
                --name=mytasks
                --jobOptions=joboptions.py
                --dataset-alias-file=dataset-alias-file.py
                [--storage-file=storage_file.pickle] (default=<name>.pickle)
  1) Create task storage file and give a name
     taskmgr.py --name=mytasks --storage-file=mytasks.pickle
  2) Dump current status
     taskmgr.py --storage-file mytasks.pickle --action=dump
  3) Define and submit pathena jobs 
     taskmgr.py -f mytasks.pickle
                --task-type=pathena \\
                --dataset-alias-file=dataset_alias_file.py \\
                --jobOptions=joboptions.py \\
                -v v1 \\
                --action=prepare,run
  3') Parse log files if for any reason one needs to do it explicitly
     taskmgr.py --storage-file mytasks.pickle --action=parse_run
  4) Update job status using pbook
     taskmgr.py --storage-file mytasks.pickle --action=update
  5) Rerun tasks (resubmit pathena jobs) for failed/cancelled jobs
     taskmgr.py --storage-file mytasks.pickle --action=rerun
  6) Dump the current status of tasks
     taskmgr.py --storage-file mytasks.pickle --action=dump
o Recover pathena job tracking
  Job submission with pathena requires athena and panda environments
  In addition to the information managed by the taskmgr, some information
  are kept in log files from various commands. They are kept under
  $TestArea/jobs where each task (=jobsets) are kept under directories
  <taskname>/run. When something goes wrong, one may recover the information by
  1) 
  taskmgr.py --name=mytasks --storage-file=mytasks.pickle
  taskmgr.py --storage-file mytasks.pickle --action=prepare,run -q
  taskmgr.py --storage-file mytasks.pickle --action=parse_run
  (repeat as many times as the number of retries)
  taskmgr.py --storage-file mytasks.pickle --action=parse_run
  taskmgr.py --storage-file mytasks.pickle --action=parse_run
  taskmgr.py --storage-file mytasks.pickle --action=update
  taskmgr.py --storage-file mytasks.pickle --action=dump
"""
def dummy():
    pass

def createSubmitScript(options):
    script = options.create_submit_script
    name = options.name
    file = '%s.pickle' % name
    jo = options.job_options
    dataset_alias_file = options.dataset_alias_file
    if options.storage_file!='': file = options.storage_file
    file = os.path.abspath(file)
    jo = os.path.abspath(jo)
    dataset_alias_file = os.path.abspath(dataset_alias_file)
    if name=='' or file=='' or jo == '' or dataset_alias_file=='':
        log.warning('Some options missing for --create-submit-script')
        log.warning('  --name=%s' % name)
        log.warning('  --jobOptions=%s' % jo)
        log.warning('  --dataset-alias-file=%s' % dataset_alias_file)
        log.warning('  [--storage-file=%s]' % file)
    #
    s = """#!/usr/bin/env zsh

name=%s
storageFile=%s
jo=%s
dataset_alias_file=%s

# 1. Create the task management file
if [[ ! -e $storageFile ]]; then
    taskmgr.py --name=$name --storage-file=$storageFile
fi

if [[ -e $dataset_alias_file ]]; then
    # Setup pathena tasks
    taskmgr.py --storage-file=$storageFile --task-type pathena --dataset-alias-file=$dataset_alias_file --jobOptions $jo --actions=prepare,run
fi
""" % (name, file, jo, dataset_alias_file)
    f = open(script, 'w')
    f.write(s)
    subprocess.call( ('chmod +x %s' % script).split())
    log.info('Created pathena submit script %s' % script)

def dummy():
    pass

def setupPathenaTasks(mgr, dataset_alias_file, jo, version='v1'):
    datasets = getDatasets(dataset_alias_file)
    if len(datasets) == 0 or jo == '':
        log.warning('Some options missing for --task-type')
        log.warning('  --dataset_alias_file=%s' % dataset_alias_file)
        log.warning('  --jobOptions=%s' % jo)
        return False
    from pathenatask import PathenaTask, PathenaTaskDefinition
    if os.path.exists(jo):
        keys = datasets.keys()
        keys.sort()
        for k in keys:
            v = datasets[k]
            jobdef = PathenaTaskDefinition(k, jo=jo, inDS=v, version=version)
            mgr.addTask(PathenaTask(jobdef))
    else:
        log.warning('JO file does not exist')
    return True

if __name__ == '__main__':
    options, args = parse_options()
    
    if options.log_level == 'INFO': log.setLevel(logging.INFO)
    elif options.log_level == 'DEBUG': log.setLevel(logging.DEBUG)
    elif options.log_level == 'WARNING': log.setLevel(logging.WARNING)
    elif options.log_level == 'ERROR': log.setLevel(logging.ERROR)
    elif options.log_level == 'FATAL': log.setLevel(logging.FATAL)

    mgr = None
    save_at_the_end = False
    if options.name != '':
        save_at_the_end = True
        mgr = TaskMgr(name=options.name, filename=options.storage_file)
    else:
        mgr = TaskMgr(filename=options.storage_file)
    if options.actions != '': save_at_the_end = True
    
    if os.path.exists(options.storage_file): mgr.load()
    mgr.options = options

    if options.task_type == 'pathena':
        'pathena'
        setupPathenaTasks(mgr, options.dataset_alias_file, options.job_options,
                          options.version)

    if options.show_examples:
        showExamples()
        log.info('Exiting now. Run again to run the tasks')
        sys.exit(0)
    if options.create_submit_script != '':
        createSubmitScript(options)
        log.info('Exiting now. Run again to run the tasks')
        sys.exit(0)

    names = []
    if len(options.task_names)>0:
        names = options.task_names.split(',')

    if options.set_status != '' and len(names)>0:
        log.info('Set status of %s to %s' % \
                 (options.task_names, options.set_status))
        for x in names:
            y = mgr.findTask(x)
            if y == None: continue
            log.info('Actually setting status of %s from %s to %s' %\
                     (x, y.status, options.set_status))
            y.status = options.set_status
            save_at_the_end = True
        pass
    
    log.info('Actions to be run: %s' % options.actions)
    if mgr.isEnabled(kUpdate): mgr.action(kUpdate, names)

    if mgr.isEnabled(kPrepare): mgr.action(kPrepare, names)
    if mgr.isEnabled(kRun): mgr.action(kRun, names)
    if mgr.isEnabled('parse_run'): mgr.action('parse_run', names)

    #if mgr.isEnabled(kUpdate): mgr.action(kUpdate, names)
    if mgr.isEnabled(kRerun): mgr.action(kRerun, names)
    if mgr.isEnabled('dump'): mgr.dump(names)
    if mgr.isEnabled('summary'): mgr.printSummary()

    if options.delete_tasks:
        log.info('Delete tasks %s' % options.task_names)
        save_at_the_end = True
        for name in names:
            mgr.deleteTask(name)
    if options.process_tasks:
        mgr.takeBestActions()
        save_at_the_end = True
    if save_at_the_end:
        mgr.save()
    
