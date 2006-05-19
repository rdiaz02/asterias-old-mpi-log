#!/usr/bin/python

import shutil
import os
import time
import glob

dirsVisit = ('/http/genesrf/www/R.running.procs',
             '/http/signs/www/R.running.procs',
             '/http/adacgh/www/R.running.procs')


MachineIP = {
    'prot01'  :  '192.168.2.1',
    'prot02'  :  '192.168.2.2',
    'prot03'  :  '192.168.2.3',
    'prot04'  :  '192.168.2.4',
    'prot05'  :  '192.168.2.5',
    'prot06'  :  '192.168.2.6',
    'prot07'  :  '192.168.2.7',
    'prot08'  :  '192.168.2.8',
    'prot09'  :  '192.168.2.9',
    'prot10'  :  '192.168.2.10',
    'prot11'  :  '192.168.2.11',
    'prot12'  :  '192.168.2.12',
    'prot13'  :  '192.168.2.13',
    'prot14'  :  '192.168.2.14',
    'prot15'  :  '192.168.2.15',
    'prot16'  :  '192.168.2.16',
    'prot17'  :  '192.168.2.17',
    'prot18'  :  '192.168.2.18',
    'prot19'  :  '192.168.2.19',
    'prot20'  :  '192.168.2.20',
    'prot21'  :  '192.168.2.21',
    'prot22'  :  '192.168.2.22',
    'prot23'  :  '192.168.2.23',
    'prot24'  :  '192.168.2.24',
    'prot25'  :  '192.168.2.25',
    'prot26'  :  '192.168.2.26',
    'prot27'  :  '192.168.2.27',
    'prot28'  :  '192.168.2.28',
    'prot29'  :  '192.168.2.29',
    'prot30'  :  '192.168.2.30',
    'prot31'  :  '192.168.2.31',
    'prot32'  :  '192.168.2.32',
    'prot33'  :  '192.168.2.33',
    'prot34'  :  '192.168.2.34',
    'prot35'  :  '192.168.2.35',
    'prot36'  :  '192.168.2.36',
    'prot37'  :  '192.168.2.37',
    'prot38'  :  '192.168.2.38',
    'prot39'  :  '192.168.2.39',
    'prot40'  :  '192.168.2.40'
    }
    
def fcheck():
    for theDir in dirsVisit:
	rrunsFiles = glob.glob(theDir + '/R.*@*%*')
	for pidMachine in rrunsFiles:
	    t1 = pidMachine.split('@')
	    t2 = t1[1].split('%')
	    Machine = t2[0]
	    pid = t2[1]
	    alive = int(os.popen("ssh " + MachineIP[Machine] + " 'ps -p " + pid + 
	    " --no-headers | wc -l'").readline())
	    if not alive:
                try:
                    os.remove(pidMachine)
                except:
                    None
                ## were we done legitimately?
                tmpDir = theDir.split('R.')[0] + 'tmp/' + t1[0].split('R.')[2]
                ## but this should not be needed, because we only
                ## look at directories with R.xyz present.
                legitimate = os.path.exists(tmpDir + "/natural.death.pid.txt") or os.path.exists(tmpDir + "/killed.pid.txt")
                
                if not legitimate:
		## write the results file
                    out1 = open(tmpDir + "/natural.death.pid.txt", mode = "w")
                    out2 = open(tmpDir + "/kill.pid.txt", mode = "w")
                    out1.write('Process died without saying goodbye!!')
                    out2.write('Process died without saying goodbye!!')
                    out1.close()
                    out2.close()
                    outf = open(tmpDir + "/pre-results.html", mode = "w")
                    outf.write("<html><head><title> Some undiagnosed problem</title></head><body>\n")
                    outf.write("<h1> Some undiagnosed problem happened</h1>")
                    outf.write(" <p> Your process died unexpectedly, without giving")
                    outf.write(" any advanced notice or leaving much trace. ")
                    outf.write(" The error is being logged, but we would also ")
                    outf.write("appreciate if you can let us know of any circumstances or problems ")
                    outf.write("so we can diagnose the error.</p>")
                    outf.write("</body></html>")
                    outf.close()
                    shutil.copyfile(tmpDir + "/pre-results.html", tmpDir + "/results.html")

fcheck()


while True:
    time.sleep(60)
    fcheck()
