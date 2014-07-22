bugfree-wookie
==============

Automatically Generate ITR Tickets!! (Service Now)

###First use!
Make sure that if you want to use the production ITR system that you have your email or functional account emailed okay'd by Rex Core or Marian Sherrin and let them know that you need a generic template with the table below.  Once they have approved your inbound email address, ITR will accept your emails with the template for this script.

Next, you will need to generate a _crendentials.py_ file which needs to contain _mail\_user_='mail username' and _mail\_pass_='mail password'.  This file is not tracked by github, but you should restrict permissions to reduce leakage.  If you need more security, feel free to fork the repo and make the necessary modifications.

####ITR Ticket Fields: [example](https://github.com/ucsc/bugfree-wookie/blob/master/test_wrapper.py)

| variable         | required | purpose           | default value              |
| ---------------- | -------- | ----------------- | -------------------------- |
| title            | yes      | Ticket title      | None                       |
| service          | yes      | Ticket Belongs to | None                       |
| sysapp           | yes      | Ticket Belongs to | None                       |
| client\_email    | no       | Client of ticket  | credentials.mail\_user     |
| assigned_to      | no       | Fixer             | None                       |
| assignment_group | no       | Fixer Group       | Help Desk                  |
| priority         | no       | Importance        | 3 (Moderate)               |
| incident_state   | no       | State             | 1 (New)                    |
| desc             | no       | Description       | None                       |
| cc               | no       | Watchlist         | None (debug=support_email) |


The values need to match up exactly with the ITR versions on service-now.  

#####create(ticket, debug=False) 
Function should be called by your external script.  debug value is used for sending test emails to ucsclearn@service-now.com.  Create is used to sanitize the inputs and return as many error codes as possible to make sure that the calling function knows that ticket was not created.  It is not possible to know that the ticket was created, no feedback is given when it is created.  In this matter, it is better to give as much feedback by erroring in the main function.

create calls both send\_email() and error\_email().  Send email is the function athat will actually send the email, and error email, will send an email to the support\_email specified if an error is raised.

####Error codes for create

| Error Code | Meaning                                             |
| ---------- | --------------------------------------------------- |
| 8          | error opening error log                             |
| 100        | title not given.                                    |
| 101        | service not given.                                  |
| 102        | sysapp not given.                                   |
| 110        | Bad email in cc list.                               |
| 111        | Error with parser on cc list.                       |
| 120        | Sending error mail failed                           |
| 130        | passed in variable was not a dictionary             |
| 200        | Error converting values of dict into strings        |

####Send\_Email(ticket, debug=False)

send mail will join the dictionary with ':' between the key and value elements for ITR to parse.  It will return an error code of 900 and 901 if an error occurs when sending the email.  If such an error occurs, error\_email() will be called.

####Error\_Email(err)

Will send an email with the error that was uncaught to the support\_email.  If this function fails, write\_error() is called, which will write the original error as well as the email error to the file error.log.


####Other comments

The fields classified as required, are not essentially required by the ITR system.  However creating a ticket without a title, a group for the ticket or a application section is not good enough for automation scripts.  If you would like to create tickets without these fields, send an email to ucsc@service-now with only the fields you need.
