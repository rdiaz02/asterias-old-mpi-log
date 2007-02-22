#!/usr/bin/python
import os
import time
import signal
import shutil
import sys
import socket
import counterApplications
import random
tmpDir = sys.argv[1]
application = sys.argv[2]


numtries = 20 ## I redefine it here. for really stubborn cases


MAX_SIMUL_RSLAVES = 16
CHECK_QUEUE = 120

def collectZombies(k = 10):
    """ Make sure there are no zombies in the process tables.
    This is probably an overkill, but works.
    """
    for nk in range(k):
        try:
            tmp = os.waitpid(-1, os.WNOHANG)
        except:
            None


## simpler if these two are cron jobs; this way, the appl. is faster.
#os.system("cd " + tmpDir + "; /http/mpi.log/buryThem.py")
#killedlamandr = os.system('/http/mpi.log/killOldLam.py')

try:
    counterApplications.add_to_log(application, tmpDir, socket.gethostname())
except:
    None

startedOK = False


### here is the "queueing" code
## FIXME: set a max time in queue, and o.w. bail out?
while True:
    num_rslaves = int(os.popen('pgrep -c Rslaves.sh').readline().split()[0])
    if num_rslaves < MAX_SIMUL_RSLAVES:
        break
    else:
        time.sleep(CHECK_QUEUE)

# time.sleep(random.uniform(0.5, 15)) ## to prevent truly simultaneous from crashing MPI

for i in range(int(numtries)):
    lamSuffix = str(int(time.time())) + str(os.getpid()) + str(random.randint(10, 9999))
    lamenvfile = open(tmpDir + '/lamSuffix', mode = 'w')
    lamenvfile.write(lamSuffix)
    lamenvfile.flush()
    lamenvfile.close()
    lamenv = os.putenv('LAM_MPI_SESSION_SUFFIX', lamSuffix)

    fullRcommand = 'export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + \
                   '"; /http/mpi.log/tryBootLAM.py ' + lamSuffix + \
                   '; cd ' + tmpDir + \
                   '; sleep 1; /http/R-custom/bin/R  --no-restore --no-readline --no-save --slave <f1.R >>f1.Rout 2>> error.msg &'
    Rrun = os.system(fullRcommand)
    time.sleep(100) ## this will always be too short if too many procs ...
    collectZombies()

    if os.path.exists(tmpDir + "/mpiOK"):
        startedOK = True
        break
    try:
        lamkill = os.system('lamhalt; lamwipe')
    except:
        None
        
    if not os.path.exists('/http/mpi.log/' + application + 'ErrorLog'):
        os.system('touch /http/mpi.log/' + application + 'ErrorLog')
    outlog = open('/http/mpi.log/' + application + 'ErrorLog', mode = 'a')
    outlog.write('MPI fails on ' + time.ctime(time.time()) +
                 ' Directory: ' + tmpDir + '\n')
    outlog.close()
   
   
if not startedOK:
    ## Logging
    if not os.path.exists('/http/mpi.log/' + application + 'ErrorLog'):
        os.system('touch /http/mpi.log/' + application + 'ErrorLog')
    outlog = open('/http/mpi.log/' + application + 'ErrorLog', mode = 'a')
    outlog.write('MPI fails on ' + time.ctime(time.time()) +
                 ' Directory: ' + tmpDir + '\n')
    outlog.close()
    ## Make sure the checkdone.cgi will stop; we create the two files here
    ## either of which will lead to loading results.html
    out1 = open(tmpDir + "/natural.death.pid.txt", mode = "w")
    out2 = open(tmpDir + "/kill.pid.txt", mode = "w")
    out1.write('MPI initialization error!!')
    out2.write('MPI initialization error!!')
    out1.close()
    out2.close()
    outf = open(tmpDir + "/pre-results.html", mode = "w")
    outf.write("<html><head><title> MPI initialization problem.</title></head><body>\n")
    outf.write("<h1> MPI initialization problem.</h1>")
    outf.write("<p> After " + numtries + " attempts we have been unable to ")
    outf.write(" initialize MPI.</p>")
    outf.write("<p> We will be notified of this error, but we would also ")
    outf.write("appreciate if you can let us know of any circumstances or problems ")
    outf.write("so we can diagnose the error.</p>")
    outf.write("</body></html>")
    outf.close()
    shutil.copyfile(tmpDir + "/pre-results.html", tmpDir + "/results.html")


