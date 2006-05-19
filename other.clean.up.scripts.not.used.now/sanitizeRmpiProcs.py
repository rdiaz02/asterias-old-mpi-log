#!/usr/bin/python

import os
import signal
import socket
import time
import re


clusterNodes = range(2, 23) + [27, 28, 30]

## First, check if any slavedemon.R is "orphan": it was created
## by an R process that no longer exists.
## Then, kill all R whose parent PID is 1. The R that are created
## by slavedemon will take this PPID when the slavedemon is killed,
## and same should happen for the R from the BATCH


####         slavedemon.R part

## two separate calls, to get rid of the calling ps and the calling grep
## if done on a single call
os.system('ps -ww -U www-data -o "%p %P %a" > tmp.ps')
os.system("grep Rslaves.sh tmp.ps > tmp2.ps")
## sure this could be dones inside Python, but awk is simpler
## for getting rid of initial spaces, unqueal spacing, etc.
os.system("awk '{print $1, $6}' tmp2.ps > tmp2b.ps")
tmp2ps = open('tmp2b.ps', mode = 'r')

if not os.path.exists('/http/mpi.log/MPI_killed_procs_' + socket.gethostname()):
    os.system('touch /http/mpi.log/MPI_killed_procs_' + socket.gethostname())
mpikilledproc = open('/http/mpi.log/MPI_killed_procs_' + socket.gethostname(), mode = 'a')
    

## often, several identical in a row.
## could use a dictiorany to make it go faste:
    ## check existece of parent only once,
    ## but kill all

killDict = {}    
while 1:
    tmpline = tmp2ps.readline()
    if not tmpline: break
    tmplist = re.split(r'[\s]+', tmpline)
    tocheck = tmplist[1].split('+')[0]
    tokill = tmplist[0]
    if killDict.has_key(tocheck):
	killDict[tocheck] = killDict[tocheck] + [tokill]
    else:
	killDict[tocheck] = [tokill]
tmp2ps.close()

testKill = killDict.keys()
for pid in testKill:
    for node in clusterNodes:
        prein = int(os.popen("ssh 192.168.2." + str(node) +
                         " 'ps -p " + pid + " --no-headers | wc -l'").readline())
        if prein > 0: break
    if prein == 1:
        del killDict[pid]
#   No, I don't want a try, 'cause I don't want to accidentally kill a proces
#   just becuase ssh failed.
#         try:
#             prein = os.popen("ssh 192.168.2." + str(node) +
#                              " 'ps -p " + pid + " --no-headers | wc -l'").readline()
#         except:
#             None
#         if prein > 0: break


testKill = killDict.keys()
for pid in testKill:
    mpikilledproc.write('Killed on ' + time.ctime(time.time()) +
	    '; machine ' + socket.gethostname() +
	    ' with parent caller ' + pid + '\n')
    for kp in killDict[pid]:
        try:
            os.kill(int(kp), signal.SIGKILL)
        except:
            None
mpikilledproc.close()


### kill all R with PPID = 1
os.system('ps -ww -U www-data -o "%p %P %a" > tmp3.ps')
os.system("grep /usr/lib/R/bin/exec/R tmp3.ps > tmp4.ps")
os.system("awk '{print $1, $2}' tmp4.ps > tmp5.ps")
tmp4ps = open('tmp5.ps', mode = 'r')

while 1:
    tmpline = tmp4ps.readline()
    if not tmpline: break
    tmplist = re.split(r'[\s]+', tmpline)
    if int(tmplist[1]) == 1:
        try:
            os.kill(int(tmplist[0]), signal.SIGKILL)
        except:
            None
tmp4ps.close()



# # while 1:
# #     tmpline = tmp2ps.readline()
# #     if not tmpline: break
# #     tmplist = re.split(r'[\s]+', tmpline)
# #     tocheck = tmplist[1].split('+')[0]
# #     if tocheck != tocheckPrevious:
# # 	inany = 0
# # 	for node in (range(2, 23) + [27, 28, 30]):
# # 	    try:
# # 		prein = os.popen("ssh 192.168.2." + str(node) +
# # 		" ps -p " + tocheck + " --no-headers | wc -l").readline()
# # 	    except:
# # 		None
# # 	    if inany > 0: break
# # ##	    else:
# # ##		inany = inany + int(prein)

# # ##	if inany == 0:
# # 	    mpikilledproc.write('Killed on ' + time.ctime(time.time()) +
# # 	    '; machine ' + socket.gethostname() +
# # 	    ' with parent caller ' + tocheck + '\n')
# # 	    try:
# # 		os.kill(int(tmplist[0]), signal.SIGKILL)
# # 	    except:
# # 		None
# #     tocheckPrevious = tocheck
