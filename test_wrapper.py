#!/usr/bin/python

import gen_ticket
import pdb

full_empty = {
  'client_email':"", # not reqr, auto sender
  'service':"ITS Internal", # returns 101
  'sysapp':"Security systems", # returns 102
  'assignment_group':"", # not reqr, Help Desk
  'assigned_to':"", # not reqr
  'priority':"", # not reqr, auto 3
  'desc':"", # not reqr
  'title':"abc", # returns 100
}

default = {
  'client_email':"",
  'service':"Security (Physical, IT & Policy)",
  'sysapp':"Network & WiFi",
  'assignment_group':"",
  'assigned_to':"",
  'priority':"2",
  'desc':"Scripted-default test",
  'title':"Script: test-defaultv3",
  'cc':'lthurlow@ucsc.edu',
}


#x1 = gen_ticket.create(full_empty,True)
x2 = gen_ticket.create(default,True)

#print "x1", x1
print "x2", x2
