#!/usr/bin/python

import shutil
import os
import time
import glob
import socket

MachineIP = [
'192.168.7.1',
'192.168.7.2',
'192.168.7.3',
'192.168.7.4',
'192.168.7.5',
'192.168.7.6',
'192.168.7.7',
'192.168.7.8',
'192.168.7.9',
'192.168.7.10',
'192.168.7.11',
'192.168.7.12',
'192.168.7.13',
'192.168.7.14',
'192.168.7.15',
'192.168.7.16',
'192.168.7.17',
'192.168.7.18',
'192.168.7.19',
'192.168.7.20',
'192.168.7.21',
'192.168.7.22',
'192.168.7.23',
'192.168.7.24',
'192.168.7.25',
'192.168.7.26',
'192.168.7.27',
'192.168.7.28',
'192.168.7.29',
'192.168.7.30',
'192.168.7.31']


for machine in MachineIP:
    try:
	trykill = os.popen("ssh " + machine + " '/http/mpi.log/killOldLam.py'")
    except:
	None

os.system('touch /http/mpi.log/completed-killOldLamAllMachines.' + socket.gethostname())
