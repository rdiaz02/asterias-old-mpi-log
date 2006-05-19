#!/usr/bin/python2.4
import sys
import os
import fcntl
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

def send_mail(email, body): 
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject']= 'Application error log'
    outer['To']= email
    #outer['CC']= email2
    outer['From']= 'pomelo2@bioinfo.cnio.es'
    outer.preamble = '\n' 
    # To guarantee the message ends with a newline
    outer.epilogue =''  
    # Note: we should handle calculating the charset
    msg= MIMEText(body) 
    # Message body
    outer.attach(msg) 
    text = outer.as_string() 
    MAIL = "/usr/sbin/sendmail"
    p = os.popen("%s -t" % MAIL, 'w')
    p.write(text)
    p.close() 
            
##############################################################################
    
# Open and read MPI error file
app_log_file = open("/http/mpi.log/snd_mpi_err")
mpi_err_text = app_log_file.read()
app_log_file.close()

# Check to see if it contains MPI errors
index = mpi_err_text.find("MPI")

# If there are no MPI errors the script must finish
if index==-1: 
    sys.exit()

# Wipe MPI error file
cf = open('/http/mpi.log/snd_mpi_err', mode = 'w')
fcntl.flock(cf.fileno(), fcntl.LOCK_SH)
cf.write("")
fcntl.flock(cf.fileno(), fcntl.LOCK_UN)
cf.close()

# Send mail with error information
send_mail('ermorrissey@cnio.es, rdiaz@cnio.es', mpi_err_text)
#send_mail('ermorrissey@cnio.es', mpi_err_text)
