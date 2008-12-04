## Keep a counter of processes launched
## We assume the file /http/log/ApplicationsCounter exists

import time
import fcntl
import os

def add_to_log(applicacion, tmpDir, hostname):
    date_time = time.strftime('%Y\t%m\t%d\t%X')    
    outstr = '%s\t%s\t%s\t%s\n' % (applicacion, date_time, hostname, tmpDir)
    cf = open('/http/mpi.log/ApplicationCounter', mode = 'a')
    fcntl.flock(cf.fileno(), fcntl.LOCK_SH)
    cf.write(outstr)
    fcntl.flock(cf.fileno(), fcntl.LOCK_UN)
    cf.close()

    
def add_to_MPIErrorLog(application, tmpDir, hostname, message = 'MPI crash'):
    if not os.path.exists('/http/mpi.log/' + application + 'MPIErrorLog'):
        os.system('touch /http/mpi.log/' + application + 'MPIErrorLog')
    outlog = open('/http/mpi.log/' + application + 'MPIErrorLog', mode = 'a')
    fcntl.flock(outlog.fileno(), fcntl.LOCK_SH)
    outlog.write(message + time.ctime(time.time()) +
                 '   Directory: ' + tmpDir +
                 '   Hostname: ' + hostname + '\n')
    fcntl.flock(outlog.fileno(), fcntl.LOCK_UN)
    outlog.close()


## the following much better from R, since we know the pid of R
## but R could fail, and we would want to see where is the lam suffix
## comming from
    
def add_to_LAM_SUFFIX_LOG(lamSuffix, application, tmpDir, hostname,
                          Rprocess = 'RprocessPid'):
    if not os.path.exists('/http/mpi.log/LAM_SUFFIX_Log'):
        os.system('touch /http/mpi.log/LAM_SUFFIX_Log')
    outlog = open('/http/mpi.log/LAM_SUFFIX_Log', mode = 'a')
    fcntl.flock(outlog.fileno(), fcntl.LOCK_SH)
    outlog.write(Rprocess + '\t' + lamSuffix + '\t' +
                 hostname + '\t' + 
                 tmpDir + '\t' +
                 '\t' + application +  '\t' + 
                 str(time.time()) + '\t' +
                 time.ctime(time.time()) + '\n')
    fcntl.flock(outlog.fileno(), fcntl.LOCK_UN)
    outlog.close()
