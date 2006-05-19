#!/usr/bin/python2.4
import sys
import os
import time
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
    #print text

def get_errors (err_name, text):
    num_errors     = text.count(err_name)
    next_err_index = 0
    err_text       = ''
    next_err       = "Pomelo II"
    # Join all errors of chosen type
    for i in range(num_errors):
        i_index        = text.find(err_name, next_err_index)
        next_err_index = text.find(next_err, i_index)
        err_text = err_text + text[i_index-30:next_err_index]

    return err_text, num_errors
        
##############################################################################


app_log_file = open("/http/mpi.log/app_caught_error")
log_text     = app_log_file.read()
app_log_file.close()

date_time = time.strftime('%Y\t%m\t%d')
new_error_tag = "Pomelo II\t" + date_time
today_index   = log_text.find(new_error_tag)


# If there are no error messages today
if today_index==-1:
    msg = "No errors were registered today " + date_time
    #send_mail('ermorrissey@cnio.es', msg) #, rdiaz@cnio.es', msg)
    print msg
    sys.exit()

# Just take todays stuff
log_text = log_text[today_index:]

# Get number of hits and text 
inp_err_text , number_input_errors   =  get_errors ("INPUT ERROR"  , log_text)
mult_err_text, number_multest_errors =  get_errors ("MULTEST ERROR", log_text)
mpi_err_text , number_mpi_errors     =  get_errors ("MPI ERROR"    , log_text)

# Get number of hits
number_url_errors      = log_text.count("URL ERROR")
number_scripts_killed  = log_text.count("POMELO KILLED")
number_server_busy     = log_text.count("SERVER BUSY")

# Statistic layout
stat_text = "\nBrief statistics (" + date_time + "):\n"
stat_text = stat_text + "POMELO II\n"
stat_text = stat_text + "-----------------------------------------------------------------\n"
stat_text = stat_text + "Number of input errors:       \t" + str(number_input_errors) + "\n"    
stat_text = stat_text + "Number of URL errors:         \t" + str(number_url_errors) + "\n"      
stat_text = stat_text + "Number of MPI errors:         \t" + str(number_mpi_errors) + "\n"      
stat_text = stat_text + "Number of multest errors:     \t" + str(number_multest_errors) + "\n"  
stat_text = stat_text + "Number of scripts killed:     \t" + str(number_scripts_killed) + "\n"  
stat_text = stat_text + "Number of server busy errors: \t" + str(number_server_busy) + "\n"     
stat_text = stat_text + "-----------------------------------------------------------------\n"


text = stat_text + inp_err_text + mult_err_text + mpi_err_text

# Silly parsing
text      = text.replace("<p>","")
text      = text.replace("</p>","\n")

print text

#send_mail('ermorrissey@cnio.es, rdiaz@cnio.es', text)
