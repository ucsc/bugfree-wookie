#!/usr/bin/python

########################################################
## TODO :
##  1. Fix all the error reporting
##      - Make it simple and easy
##  2. Think about the write to a file and clear, if
##     used heavily, this will create issues with others


import logging
import smtplib
import traceback
import email.mime.text
import pdb
import sys
import re

## Check if we have a credentials file, explain for new
## users unfamiliar with python, how to generate this file
try:
  import credentials
except Exception:
  sys.stderr.write("credentials.py was not found!\n")
  sys.stderr.write("Create a file called credentials.py"\
                   " in this directory\n")
  sys.stderr.write("contents:\n")
  sys.stderr.write("#!/usr/bin/python\n")
  sys.stderr.write("\n")
  sys.stderr.write("mail_user=\'\'\n")
  sys.stderr.write("mail_pass=\'\'\n")
  sys.stderr.write("\n")
  sys.stderr.write("between \'\' input the username and password.\n")
  sys.exit(1)

## Long Term Support for this script.
support_email="lthurlow@ucsc.edu"

## Email didnt work, so write to disk.
def write_error(err_a, err_b):
  file_err = open("error.log","wb")
  ## Two types of error can occur, both can be null
  if err_a:
    file_err.write("Email Error:\n")
    for item in err_a:
      file_err.write(item+":\n"+err_a[item]+"\n")
  if err_b:
    file_err.write("Code Error:\n")
    for item in err_b:
      file_err.write(item+":\n"+err_b[item]+"\n")
  file_err.close()

## something in our code broke, send an email to LTS script
## owner, so that they can patch the error.
def email_error(err):
  try:
    mailserv = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    mailserv.login(credentials.mail_user,\
                   credentials.mail_pass)
    msg = email.mime.text.MIMEText(str(err[1]))
    To = support_email
    From = credentials.mail_user
    msg["To"] = To
    msg["From"] = From
    date_today = datetime.date.today().strftime("%m/%d/%y")
    msg["Subject"] = "Error Auto-Generating Ticket: %s"\
                     % date_today
    mailserv.sendmail(From, To, msg.as_string())
    mailserv.quit()
    return {'ret':0}
  except Exception as e:
    return {'ret':1,'error':str(e),\
            'trace':traceback.format_exc()}

## Send the ITR email to generate a ticket
## Assumption: this should not fail unless it is mail
## related, all fields should have been satized before
## being sent to this function.
def send_email(ticket, debug=False):
  try:
    mailserv = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    mailserv.login(credentials.mail_user,\
                   credentials.mail_pass)

    sep = ":"
    nl = "\n"
    ## Creating ticket format
    try:
      msg_str = \
                "client_email"+sep+ticket["client_email"]+nl+\
                "service"+sep+ticket["service"]+nl+\
                "sysapp"+sep+ticket["sysapp"]+nl+\
                "assignment_group"+sep+ticket["assignment_group"]+nl+\
                "assigned_to"+sep+ticket["assigned_to"]+nl+\
                "priority"+sep+ticket["priority"]+nl+\
                "incident_state"+sep+ticket["incident_state"]+nl+\
                "Description:"+nl+\
                "watchlist:"+str(ticket["cc"])+nl+\
                ticket["desc"]+nl+\
                nl+\
                "This ticket has been auto-generated, if an error has "+\
                "occured, please contact: %s" % support_email
   
    except Exception as e:
      ## email error to support
      ret_code = email_error((traceback.format_exc(),e))
      if ret_code['ret'] > 0:
        orig_fail = (traceback.format_exc(),e)
        write_error(ret_code, orig_fail)
        return 900
      else:
        return 901
 
    ## This is where I would suspect the function to fail.
    try:
      msg = email.mime.text.MIMEText(msg_str)
      # Email Header Information
      To = support_email
      Cc = ""
      if debug:
        if ticket["cc"]:
          Cc = '%s,%s' % (ticket["cc"],support_email)
        else:
          Cc = support_email
        To = "ucsclearn@service-now.com"
        msg["To"] = To
        msg["Cc"] = Cc
      else:
        Cc = ticket["cc"]
        To = "ucsc@service-now.com"
        msg["To"] = To
        msg["Cc"] = Cc
      From = credentials.mail_user
      msg["From"] = From
      msg["Subject"] = str(ticket["title"])
      mailserv.sendmail(From, [To,Cc], msg.as_string())
    except Exception as e:
      ## email error to support
      ret_code = email_error((traceback.format_exc(),e))
      if ret_code['ret'] > 0:
        orig_fail = (traceback.format_exc(),e)
        write_error(ret_code, orig_fail)
        return ret_code
    mailserv.quit()

  ## Some bizzare un-caught exception.
  except Exception as e:
    orig_fail = (traceback.format_exc(),e)
    write_error(None, orig_fail)
    return 600

  return 0


# Create a new ticket, ONLY VERIFY contents.
def create(tick_dict, DEBUG=False):
  ## clear the error.log file
  try:
    file_err = open("error.log","wb")
    file_err.close()
  except Exception:
    return 8
  if type(tick_dict) == dict:
    try:
      ## Force all values to be strings
      for k in tick_dict.keys():
        if type(tick_dict[k]) != str:
          tick_dict[k] = str(tick_dict[k])

      ## should not be able to create ticket without subject
      if not tick_dict['title']:
        return 100
      ## A service is required.
      if not tick_dict['service']:
        return 101
      ## also required from ITR
      if not tick_dict['sysapp']:
        return 102
    ## These fields are required to be passed in, if not
    ## we should error
    except Exception:
      return 200

    ## Either have this script be the client
    ## or use given
    if 'client_email' not in tick_dict.keys():
      tick_dict['client_email'] = credentials.mail_user
    elif not tick_dict['client_email']:
      tick_dict['client_email'] = credentials.mail_user

    ## if no priority given, set to moderate
    if 'priority' not in tick_dict.keys():
      tick_dict['priority'] = '3'
    elif not tick_dict['priority']:
      tick_dict['priority'] = '3'
    ## If we werent given who to assign this ticket to
    ## We need assign to Help Desk
    if "assignment_group" not in tick_dict.keys():
      tick_dict["assignment_group"] = "Help Desk"
    ## Or given no group -> help desk
    elif not tick_dict["assignment_group"]:
      tick_dict["assignment_group"] = "Help Desk"

    if "cc" not in tick_dict.keys():
      tick_dict["cc"] = []
    elif tick_dict["cc"]:
      try:
        expr = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
        for cc in tick_dict["cc"].split(','):
          if not re.findall(expr,cc):
            return 110 # invalid email addr
      except Exception:
       return 111

    ## set to new if not given
    tick_dict['incident_state'] = '1'
    if 'desc' not in tick_dict.keys():
      tick_dict['desc'] = ""
 
    ##limit subject size.
    if len(str(tick_dict['title'])) > 99:
      tick_dict['title'] = tick_dict['title'][:99]
    ##limit description size.
    if len(str(tick_dict['desc'])) > 3800:
      tick_dict['desc'] = tick_dict['desc'][:3800]
    

    ## All else is fine, time to ship it.
    try:
      ret_code = send_email(tick_dict, DEBUG)
      return ret_code
      ## ITR generation wont give us INC number, so best we can
      ## do is let the owners know that it succeeded.
    except Exception:
      return 120
     
  else:
    ## if another language is used, write function here to catch
    ## and re-call create funct. recursively / JSON
    ## TODO: This whole segment
    return 130

## TODO: KB0017170 implementation
## Just for SOE -> 48/22 and 5/24 
def assign_group(ip=None,hostname=None):
  if type(ip) == str:
    ip_dom = int(ip.split('.')[2])
    if ip_dom == 5 or (ip_dom >= 48 and ip_dom <= 51):
      return "SOE"
  if type(hostname) == str:
    domain = hostname.split('.').split('-')
    if "eduroam" in domain:
      return "eduroam"
    elif "cruznet" in domain:
      return "cruznet"
    elif "resnet" in domain:
      return "resnet"
    elif "fsh" in domain:
      return "fsh"
    elif "dhcp" in domain:
      return None
  return None
