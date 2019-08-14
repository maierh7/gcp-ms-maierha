#! /usr/bin/env python3

import re
import os
import sys

import opt
import sub
import subprocess

opt.RemoveServ ()
opt.parser.add_option ("-l", "--list", default=False, action="store_true", dest="list")
opt.parser.add_option ("-c", "--cur",  default=False, action="store_true", dest="cur")
opt.parser.add_option ("-a", "--acc",  default=False, action="store_true", dest="acc")
opt.parser.add_option ("-p", "--pro",  dest="pro")
opt.parser.add_option ("-s", "--sql",  default=False, action="store_true", dest="sql")

(opts, args) = opt.GetOptions ()
lst = dict ()
cur = ""

sqlp = {
    "V135-5256-Playground-HaraldMai" : "v135-5256-playground-haraldmai",
    "V135-playground-mai-dev" :        "xbbcvpbxkziv",
    "6117V135-myaccount-prod" :        "aq12fq1g0adk",
    "6117V135-myaccount-dev"  :        "u1f3rwmxbxdt",
    }

def get_cur_pro ():
    out = subprocess.check_output ("gcloud config get-value project", 
                                       shell=True).decode ('utf-8')
    lines = out.splitlines ()
    for i in lines:
        global cur
        cur = i

def get_projects ():
    out = subprocess.check_output ("gcloud projects list", shell=True).decode ('utf-8')
    lines = out.splitlines()
    flag = False
    for i in lines:
        arr = re.split ("\s+", i)
        if arr[0] == cur:
            i = i + " *"
        if flag is True:
            lst [arr[0]] = i
        flag = True

def set_project ():
    os.system ("gcloud config set project " + opts.pro)
    out = subprocess.check_output ("gcloud config get-value project", shell=True).decode ('utf-8')
    lines = out.splitlines ()
    for i in lines:
        print (i)        

def get_sql_project ():
    idx = 0
    for i in sqlp:
        idx = idx +1
        print ("%2d %30s %30s" % (idx, i, sqlp[i]))
    sel = int (input ("Get index: "))
    pro = list (sqlp.keys ())[sel-1]
    opts.pro = sqlp[pro]
    set_project ()
        
if opts.sql:
    get_sql_project ()
    sys.exit (0)

get_cur_pro ()
get_projects ()
print ("cur:", cur)

if opts.cur is False and opts.acc is False and opts.list is False and opts.pro is False:
    opts.list = True

if opts.list:
    for i in sorted (lst):
        lin = lst[i]
        if len (args):
            for j in args:
                m = re.search (j, lin)
                if m:
                    print (lin)
        else:
            print (lin)

if opts.cur:
    sub.out_cmd ("gcloud config get-value project")    

if opts.acc:
    sub.out_cmd ("gcloud config get-value account")

if opts.pro:
    set_project ()
