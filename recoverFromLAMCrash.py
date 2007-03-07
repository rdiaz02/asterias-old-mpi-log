#!/usr/bin/python



import sys
import os
import time
import glob

tmpDir = sys.argv[1]

machine_root = 'karl'
TIME_BETWEEN_CHECKS = 120


def lamboot(lamSuffix):
    'Boot a lam universe'
    fullCommand = 'export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + \
                  '"; /http/mpi.log/tryBootLAM.py ' + lamSuffix
    lboot = os.system(fullCommand)

def check_tping(lamSuffix, tmpDir, tsleep = 15, nc = 2):
    """ Use tping to verify LAM universe OK.
    tsleep is how long we wait before checking output of tping.
    Verify also using 'lamexec C hostname' """
    
    tmp2 = os.system('export LAM_MPI_SESSION_SUFFIX="' +\
                     lamSuffix + '"; cd ' + tmpDir + \
                     '; tping C N -c' + str(nc) + \
                     ' > tping.out & ')
    time.sleep(tsleep)
    tmp = int(os.popen('cd ' + tmpDir + \
                       '; wc tping.out').readline().split()[0])
    os.system('rm ' + tmpDir + '/tping.out')
    timeHuman = '##########   ' + \
                str(time.strftime('%d %b %Y %H:%M:%S')) 
    os.system('echo "' + timeHuman + \
              '" >> ' + tmpDir + '/checkTping.out')
    if tmp == 0:
        os.system('echo "tping fails" >> ' + \
                  tmpDir + '/checkTping.out')
        return 0
    elif tmp > 0:
        os.system('echo "tping OK" >> ' + \
                  tmpDir + '/checkTping.out')
        lamexec = os.system('export LAM_MPI_SESSION_SUFFIX="' +\
                            lamSuffix + '"; lamexec C hostname')
        if lamexec == 0:
            os.system('echo "lamexec OK" >> ' + \
                      tmpDir + '/checkTping.out')
            return 1
        else:
            os.system('echo "lamexec fails" >> ' + \
                      tmpDir + '/checkTping.out')
            return 0
    else:
        os.system('echo "tping weird ' + str(tmp) + '" >> ' + \
                  tmpDir + '/checkTping.out')
        return 0



def recover_from_lam_crash(tmpDir, machine_root = machine_root,
                           tsleep = 100, maxrmpi_tries = 10):
    """Check if lam crashed during R run. If it did, restart R
    after possibly rebooting the lam universe.
    Leave a trace of what happened."""
    final_value = 'NoCrash'
    OTHER_LAM_MSGS = 'Call stack within LAM:'
    lam_logs = glob.glob(tmpDir + '/' + machine_root + '*.*.*.log')
    in_error_msg = int(os.popen('grep MPI_Error_string ' + \
                                tmpDir + '/error.msg | wc').readline().split()[0])
    if in_error_msg > 0:
        os.system('rm ' + tmpDir + '/error.msg')
        for lam_log in lam_logs:
            os.system('rm ' + lam_log)
    else: ## look in lam logs
        in_lam_logs = 0
        for lam_log in lam_logs:
            tmp1 = int(os.popen('grep "' + OTHER_LAM_MSGS + '" ' + \
                                lam_log + ' | wc').readline().split()[0])
            if tmp1 > 0:
                in_lam_logs = 1
                for lam_log in lam_logs: os.system('rm ' + lam_log)
                break

    if (in_error_msg > 0) or (in_lam_logs > 0):
        final_value = 'Recovering'
        os.system('mv ' + tmpDir + '/mpiOK ' + tmpDir + '/previous_mpiOK')
        timeHuman = str(time.strftime('%d %b %Y %H:%M:%S')) 
        os.system('echo "' + timeHuman + \
                  '" >> ' + tmpDir + '/recoverFromLAMCrash.out')
        lamSuffix = open(tmpDir + "/lamSuffix", mode = "r").readline()
        lam_ok = check_tping(lamSuffix, tmpDir)
        if lam_ok == 0: lboot = lamboot(lamSuffix)
        Rcommand = 'export LAM_MPI_SESSION_SUFFIX="' + lamSuffix + \
                   '"; cd ' + tmpDir + \
                   '; sleep 1; /http/R-custom/bin/R --no-readline --no-save --slave <f1.R >>f1.Rout 2>> error.msg &'
        Rrun = os.system(Rcommand)
        ## Verify Rmpi started OK, and relaunch o.w.
        for rmpytry in range(maxrmpi_tries):
            time.sleep(tsleep)
            if os.path.exists(tmpDir + "/mpiOK"):
                startedOK = True
                break
            else:
                startedOK = False
                lam_ok = check_tping(lamSuffix, tmpDir)
                if lam_ok == 0: lboot = lamboot(lamSuffix)
                Rrun = os.system(Rcommand)

        if startedOK == False: ## something seriously broken: give up.
            final_value = 'FAILED'
    timeHuman = str(time.strftime('%d %b %Y %H:%M:%S')) 
    os.system('echo "' + final_value + '  at ' + timeHuman + \
              '" >> ' + tmpDir + '/recoverFromLAMCrash.out')
    return final_value




while True:
    lam_recovered = recover_from_lam_crash(tmpDir)
    time.sleep(TIME_BETWEEN_CHECKS)
