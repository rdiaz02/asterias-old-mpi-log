#!/usr/bin/python
import counterApplications
import socket
import sys

appl = sys.argv[1]
tmpDir = sys.argv[2]

try:
    counterApplications.add_to_log(appl, tmpDir, socket.gethostname())
except:
    None
