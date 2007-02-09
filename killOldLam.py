#!/usr/bin/env python

"""
Kills lamds and Rs longer than 24 hours run by the user in charge of the we app.
we use an ugly hack: bsdstart returns the duration of a process as HH:MM only if
less < 24. Thus, we just check for the precessend of ':' in the given field."""


import os

## Read configuration options
# from ConfigParser import ConfigParser
# config = ConfigParser()
# config.read('../../asterias_config2.ini')
# try:
#     USER = eval(config.get('MPI_config', 'USER'))
# except:
#     print 'USER ([MPI_config] in asterias_config2.ini) evaluation error. \
#     It should be a (Python) string.'

USER = 'www-data'


lamds_running = os.popen('ps -C lamd -o pid,user,bsdstart h').readlines()
Rs_running    = os.popen('ps -C R -o pid,user,bsdstart h').readlines()

for proc_line in lamds_running:
    proc_break = proc_line.strip().split()
    if (proc_break[1] == USER) and (proc_break[2].find(':') == -1):
	os.system('kill -s 9 ' + str(int(proc_break[0])))

for proc_line in Rs_running:
    proc_break = proc_line.strip().split()
    if (proc_break[1] == USER) and (proc_break[2].find(':') == -1):
	os.system('kill -s 9 ' + str(int(proc_break[0])))

