#!/usr/bin/python2.4

""" Better to do this periodically, than to ask the cgi.
cgi can spend a lot doing this sort of thing and it shouldn't. """


import dircache
import shutil
import os
import time
import socket

MAX_time = 3600 * 24 * 5

def delete_old(location):
    currentTime = time.time()
    currentTmp = dircache.listdir(location)    
    for directory in currentTmp:
        tmpS = location +"/" + directory
        if (currentTime - os.path.getmtime(tmpS)) > MAX_time:
            try:
                shutil.rmtree(tmpS)
            except:
                try: 
                    os.remove(tmpS) ## if it is a file
                except:
                    None


## expanded to include R.running.procs
dirs_to_clean = ('/http/pomelo2/www/tmp',
                 '/http/tnasas/www/tmp',
                 '/http/signs2/www/tmp',
                 '/http/genesrf2/www/tmp',
                 '/http/adacgh2/www/tmp',
                 '/http/prep/www/tmp',
                 '/http/signs2/www/R.running.procs',
                 '/http/genesrf2/www/R.running.procs',
                 '/http/adacgh2/www/R.running.procs'
##                 '/http/prep/www/tmp'
                 )


for this_dir in dirs_to_clean:
    delete_old(this_dir)

os.system('touch /http/mpi.log/completed-delete-old-dirs.' + socket.gethostname())
