#!/usr/bin/python

## kills lamds longer than 24 hours. For now I don't verify user
## also kills old Rs. Again, for now don't verify user
import os
lamds_running_pid = os.popen('ps -C lamd -o pid h').readlines()
lamds_running_start = os.popen('ps -C lamd -o bsdstart h').readlines()
lamds_running_user = os.popen('ps -C lamd -o user h').readlines()

k = -1
for lamd in lamds_running_start:
    k = k + 1
    if lamd.find(':') == -1:
	pid = lamds_running_pid[k]
	os.system('kill -s 9 ' + str(int(pid)))
	#print 'kill this ' + pid

Rs_running_pid = os.popen('ps -C R -o pid h').readlines()
Rs_running_start = os.popen('ps -C R -o bsdstart h').readlines()
Rs_running_user = os.popen('ps -C R -o user h').readlines()


k = -1
for R in Rs_running_start:
    k = k + 1
    if R.find(':') == -1:
	pid = Rs_running_pid[k]
	os.system('kill -s 9 ' + str(int(pid)))
	#print 'kill this ' + pid

