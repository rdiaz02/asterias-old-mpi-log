#!/usr/bin/python
import os
import time
import socket
import random

numtries = 20 ## I redefine it here. for really stubborn cases

MIN_LAM_NODES = 15 ## highly deployment dependant. But in our clusters

for ntr in range(numtries):
    tmp = os.system('/usr/bin/lamboot -H /http/mpi.defs/lamb-host.' + socket.gethostname() + '.def')
    os.sleep(1)
    if (tmp == 0) and \
           (int(os.popen('lamnodes | wc').readline().split()[0]) > MIN_LAM_NODES):
        break
    time.sleep(1 + random.uniform(1, 12))
