#!/usr/bin/python

import gen_ticket

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
  'title':"Script: test-defaultv1",
}


x1 = gen_ticket.create(full_empty)
#x2 = gen_ticket.create(default)

print "x1", x1
#print "x2", x2
