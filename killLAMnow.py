#!/usr/bin/python
## Kill lam immeidately given the IP and suffix
## CGI no longer running.
import os
import time
import sys

machine = '192.168.2.' + sys.argv[1]
lamenv = sys.argv[2]


try:
    os.system("ssh " + machine + " 'export LAM_MPI_SESSION_SUFFIX=" + lamenv +
              "; lamhalt -H; lamwipe -H'")
except:
    None

