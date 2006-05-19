#!/usr/bin/python
import os
import time

clusterNodes = range(2, 23) + [27, 28, 30]


while True:
    for node in clusterNodes:
        time.sleep(5)
        try:
            kk = os.system("ssh 192.168.2." + str(node) + 
                           " '/http/mpi.log/sanitizeRmpiProcs.py'")
        except:
            None
	
