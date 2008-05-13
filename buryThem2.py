#!/usr/bin/python

import shutil
import os
import time
import glob

dirsVisit = ('/http/signs2/www/R.running.procs','/http/adacgh2/www/R.running.procs',
	     '/http/genesrf2/www/R.running.procs')
#     '/http/signs2/www/R.running.procs',
#     '/http/adacgh2/www/R.running.procs')


commonRoute = 'R.running.procs'


## FIXME: we'll need to fix this later: generate dictionary

MachineIP = {
    'karl01'  :  '192.168.7.1',
    'karl02'  :  '192.168.7.2',
    'karl03'  :  '192.168.7.3',
    'karl04'  :  '192.168.7.4',
    'karl05'  :  '192.168.7.5',
    'karl06'  :  '192.168.7.6',
    'karl07'  :  '192.168.7.7',
    'karl08'  :  '192.168.7.8',
    'karl09'  :  '192.168.7.9',
    'karl10'  :  '192.168.7.10',
    'karl11'  :  '192.168.7.11',
    'karl12'  :  '192.168.7.12',
    'karl13'  :  '192.168.7.13',
    'karl14'  :  '192.168.7.14',
    'karl15'  :  '192.168.7.15',
    'karl16'  :  '192.168.7.16',
    'karl17'  :  '192.168.7.17',
    'karl18'  :  '192.168.7.18',
    'karl19'  :  '192.168.7.19',
    'karl20'  :  '192.168.7.20',
    'karl21'  :  '192.168.7.21',
    'karl22'  :  '192.168.7.22',
    'karl23'  :  '192.168.7.23',
    'karl24'  :  '192.168.7.24',
    'karl25'  :  '192.168.7.25',
    'karl26'  :  '192.168.7.26',
    'karl27'  :  '192.168.7.27',
    'karl28'  :  '192.168.7.28',
    'karl29'  :  '192.168.7.29',
    'karl30'  :  '192.168.7.30',
    'karl31'  :  '192.168.7.31'
    }

def R_done(tmpDir):
    """Verify if Rout exists. If it does, see if done"""
##    rfile = 1
    try: 
	Rrout = open(tmpDir + "/f1.Rout")
    except:
	return 1
    if os.path.exists(tmpDir + '/RterminatedOK'):
        return 1
##    if rfile:
    soFar = Rrout.read()
    Rrout.close()
    finishedOK = soFar.endswith("Normal termination\n")
    errorRun = soFar.endswith("Execution halted\n") ## might interact badly with relaunching lam
    if finishedOK or errorRun:
        return 1
    else:
        return 0
    
def fcheck():
    for theDir in dirsVisit:
	rrunsFiles = glob.glob(theDir + '/R.*@*%*')
	for pidMachine in rrunsFiles:
	    t1 = pidMachine.split('@')[0].split('/R.')[-1]
            thisDir = theDir.replace(commonRoute, '') + 'tmp/' + t1
            machine, pid = open(thisDir + '/current_R_proc_info',
                                mode = 'r').readlines()[0].split()
	    alive = int(os.popen("ssh " + machine + " 'ps -p " + pid + \
                                 " --no-headers | wc -l'").readline())
	    if not alive:
                try:
                    os.remove(pidMachine)
                except:
                    None
                ## were we done legitimately?
		## recall natural.death.pid and killed.pid only created after every 30" check.
		## But python or the shell can take a while to complete several operations
		## 
		legitimate = os.path.exists(thisDir + "/natural.death.pid.txt") or os.path.exists(thisDir + "/killed.pid.txt") or R_done(thisDir)
                
                if not legitimate:
		## write the results file
                    out1 = open(thisDir + "/natural.death.pid.txt", mode = "w")
                    out2 = open(thisDir + "/kill.pid.txt", mode = "w")
                    out1.write('Process died without saying goodbye!!')
                    out2.write('Process died without saying goodbye!!')
                    out1.close()
                    out2.close()
                    outf = open(thisDir + "/pre-results.html", mode = "w")
                    outf.write("<html><head><title> Some undiagnosed problem</title></head><body>\n")
                    outf.write("<h1> Some undiagnosed problem happened</h1>")
                    outf.write(" <p> Your process died unexpectedly, without giving")
                    outf.write(" any advanced notice or leaving much trace. ")
                    outf.write(" The error is being logged, but we would also ")
                    outf.write("appreciate if you can let us know of any circumstances or problems ")
                    outf.write("so we can diagnose the error.</p>")
                    outf.write("</body></html>")
                    outf.close()
                    shutil.copyfile(thisDir + "/pre-results.html", thisDir + "/results.html")

fcheck()
