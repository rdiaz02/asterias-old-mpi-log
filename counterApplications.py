## Keep a counter of processes launched
## We assume the file /http/log/ApplicationsCounter exists

import time
import fcntl

def add_to_log(applicacion, tmpDir, hostname):
    date_time = time.strftime('%Y\t%m\t%d\t%X')    
    outstr = '%s\t%s\t%s\t%s\n' % (applicacion, date_time, hostname, tmpDir)
    cf = open('/http/mpi.log/ApplicationCounter', mode = 'a')
    fcntl.flock(cf.fileno(), fcntl.LOCK_SH)
    cf.write(outstr)
    fcntl.flock(cf.fileno(), fcntl.LOCK_UN)
    cf.close()

    
