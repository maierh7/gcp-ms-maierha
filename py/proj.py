#! /usr/bin/env python3

import re
import os
import sys

import opt
import sub
import subprocess

opt.parser.add_option ("-l", "--list", default=False, action="store_true", dest="list")
opt.parser.add_option ("-c", "--cur",  default=False, action="store_true", dest="cur")
opt.parser.add_option ("-a", "--acc",  default=False, action="store_true", dest="acc")
opt.parser.add_option ("-p", "--pro",  default=False, action="store_true", dest="pro")

(opts, argv) = opt.GetOptions ()
lst = list ()

def set_project ():
    out = subprocess.check_output ("gcloud projects list", shell=True).decode ('utf-8')
    lines = out.splitlines()
    flag = False
    for i in lines:
        arr = re.split ("\s+", i)
        if flag is True:
            lst.append (arr[0])
        flag = True
    it = 0
    for i in lst:
        print (it, i)
        it = it + 1
    res = input("read number:")
    os.system ("gcloud config set project " + lst[int (res)])
    sub.out_cmd ("gcloud config get-value project")

if opts.cur is False and opts.acc is False and opts.list is False and opts.pro is False:
    opts.list = True

if opts.list:
    sub.out_cmd ("gcloud projects list")

if opts.cur:
    sub.out_cmd ("gcloud config get-value project")    

if opts.acc:
    sub.out_cmd ("gcloud config get-value account")

if opts.pro:
    set_project ()
    
