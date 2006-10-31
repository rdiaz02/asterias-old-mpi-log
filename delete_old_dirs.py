#!/usr/bin/python2.4

""" Better to do this periodically, than to ask the cgi.
cgi can spend a lot doing this sort of thing and it shouldn't. """


import dircache
import shutil
import os
import time

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



dirs_to_clean = ('/http/pomelo2/www/tmp',
                 '/http/tnasas/www/tmp',
                 '/http/signs/www/tmp',
                 '/http/genesrf/www/tmp',
                 '/http/adacgh/www/tmp',
                 '/http/prep/www/tmp',
                 '/http/dnmad/www/temp')


for this_dir in dirs_to_clean:
    delete_old(this_dir)


