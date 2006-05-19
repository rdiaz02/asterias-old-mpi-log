#!/usr/bin/python
## Kill lam; used by calling from R, so that lam is killed even if
## CGI no longer running.
import os
import time
import sys

lamenv = sys.argv[1]
time.sleep(100) ## wait, just in case CGI is really running

try:
    os.system('export LAM_MPI_SESSION_SUFFIX=' + lamenv +
              '; lamhalt -H; lamwipe -H')
except:
    None

