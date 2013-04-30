#!/usr/bin/python
import os
import time
import socket
import random
import sys

lamSuffix = sys.argv[1]
onlyTen = sys.argv[2]

numtries = 20

MIN_LAM_NODES = 15 ## highly deployment dependant. But in our clusters

## Note: It would be nicer if, on failure after 20 tries, we could signal
## the error and pass it to tryRrun3.py. Now, after the 20 tris, we
## nevertheless go and start R, and failure is there.
## I have a fever now, and can't think about it. FIXME

def create_onlyTen(name):



if onlyTen:
    for ntr in range(numtries):
        create_onlyTen(socket.gethostname())

        ##print 'doing ntr ' + str(ntr)
        tmp = os.system('export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + \
                        '"; /usr/bin/lamboot -H /http/mpi.defs/lamb-host.' + \
                        socket.gethostname() + '.onlyten.1cpu.def 2>/dev/null')
        time.sleep(1)
        if (tmp == 0) and \
               (int(os.popen('export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + \
                             '"; lamnodes | wc').readline().split()[0]) > MIN_LAM_NODES):
            break
        time.sleep(1 + random.uniform(1, 12))

else:
    for ntr in range(numtries):
        ##print 'doing ntr ' + str(ntr)
        tmp = os.system('export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + \
                        '"; /usr/bin/lamboot -H /http/mpi.defs/lamb-host.' + \
                        socket.gethostname() + '.1cpu.def 2>/dev/null')
        time.sleep(1)
        if (tmp == 0) and \
               (int(os.popen('export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + \
                             '"; lamnodes | wc').readline().split()[0]) > MIN_LAM_NODES):
            break
        time.sleep(1 + random.uniform(1, 12))
