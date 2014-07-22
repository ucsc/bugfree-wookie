bugfree-wookie
==============

Automatically Generate ITR Tickets!! (Service Now)

ITR Ticket Fields: [example](https://github.com/ucsc/bugfree-wookie/blob/master/test_wrapper.py)

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

create(ticket, debug=False) function should be called by your external script.  debug value is used for sending test emails to ucsclearn@service-now.com.  Create is used to sanitize the inputs and return as many error codes as possible to make sure that the calling function knows that ticket was not created.  It is not possible to know that the ticket was created, no feedback is given when it is created.  In this matter, it is better to give as much feedback by erroring in the main function.

create calls both send\_email() and error\_email().  Send email is the function athat will actually send the email, and error email, will send an email to the support\_email specified if an error is raised.

Error codes for create()

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


