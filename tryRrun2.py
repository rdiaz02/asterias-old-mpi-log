#!/usr/bin/python
import os
import time
import signal
import shutil
import sys
import socket
import counterApplications
import whrandom
tmpDir = sys.argv[1]
numtries = sys.argv[2]
application = sys.argv[3]

# def tryRrun(Rcommand, tmpDir, numtries = 10, application = "SignS")
#     """ Try to launch R via os.system, verifying MPI got initialized.
#     We try to initiate R up to numtries times; we verify MPI (or Snow)
#     got initialized correctly (that requires that R produces an mpiOK file).
#     If it doesn't, we call the mpi sanitization scripts to do their job
#     and try again.
#     """

def collectZombies(k = 10):
    """ Make sure there are no zombies in the process tables.
    This is probably an overkill, but works.
    """
    for nk in range(k):
        try:
            tmp = os.waitpid(-1, os.WNOHANG)
        except:
            None


## The following does not work. We would need to caputer the output
## from ps, and then get substring with -sessionsuffix and the number = lamSuffix.
## But killing lam kills all slaves and the main process
## lamdpid = os.popen('ps --ppid ' + str(lampid) + ' -o "%p" --no-headers').readline()
## time.sleep(0.5)

os.system("cd " + tmpDir + "; /http/mpi.log/buryThem.py")
#os.system("cd " + tmpDir + "; /http/mpi.log/sanitizeRmpiProcs.py")

killedlamandr = os.system('/http/mpi.log/killOldLam.py')

try:
    counterApplications.add_to_log(application, tmpDir, socket.gethostname())
except:
    None

startedOK = False
for i in range(int(numtries)):

    lamSuffix = str(os.getpid()) + str(whrandom.randint(1, 999999))
    lamenvfile = open(tmpDir + '/lamSuffix', mode = 'w')
    lamenvfile.write(lamSuffix)
    lamenvfile.flush()
    lamenvfile.close()
    lamenv = os.putenv('LAM_MPI_SESSION_SUFFIX', lamSuffix)
#     lampid = os.spawnlp(os.P_NOWAITO,
#                         '/usr/bin/lamboot',
#                         '/usr/bin/lamboot',
#                         '/http/mpi.defs/lamb-host.' + socket.gethostname() + '.def')

#     Rcommand = "cd " + tmpDir + "; " + "/usr/bin/R  --no-restore --no-readline --no-save --slave <f1.R >f1.Rout 2> error.msg &"

#    Rrun = os.system(Rcommand)


    fullRcommand = 'export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + '";' + '/usr/bin/lamboot -H /http/mpi.defs/lamb-host.' + socket.gethostname() + '.def; cd ' + tmpDir + '; ' + '/usr/bin/R  --no-restore --no-readline --no-save --slave <f1.R >f1.Rout 2> error.msg &'
    Rrun = os.system(fullRcommand)
    time.sleep(30)
    collectZombies()

    if os.path.exists(tmpDir + "/mpiOK"):
        startedOK = True
#         lamenvfile = open(tmpDir + '/lamSuffix', mode = 'w')
#         lamenvfile.write(lamSuffix)
#         lamenvfile.close()
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


