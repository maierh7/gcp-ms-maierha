#! /usr/bin/env python3

import re
import subprocess

import opt
import sub

opt.parser.add_option ("", "--list",  default=False, action="store_true", dest="list")
opt.parser.add_option ("", "--stop",  default=False, action="store_true", dest="stop")
opt.parser.add_option ("", "--start", default=False, action="store_true", dest="start")


(opts, args) = opt.GetOptions ()
lst = dict ()

def get_inst_list ():
    out = subprocess.check_output ("gcloud compute instances list", shell=True).decode ("utf-8")
    lin = out.splitlines ()

    flag = False
    for i in lin:
        if flag == True:
            res = re.split(" +", i)
            lst [res[0]] = res[1]
        flag = True

def print_lst ():
    cnt = 0
    for i in lst:
        print ("%2d %-20s %s" % (cnt, i, lst[i]))
        cnt += 1
    res = input ("Read Number:")
    return res

def get_index (ind):
    cnt = 0
    for i in lst:
        if cnt == ind:
            return (i, lst[i])
        cnt += 1

get_inst_list ()

if opts.list == True:
    sub.out_cmd("gcloud compute instances list")

if opts.start == True:
    (host, zone) = get_index (int (print_lst ()))
    cmd = "gcloud compute instances start " + host + " --zone=" + zone
    subprocess.run (cmd, shell=True)

if opts.stop == True:
    (host, zone) = get_index (int (print_lst ()))
    cmd = "gcloud compute instances stop " + host + " --zone=" + zone
    subprocess.run (cmd, shell=True)

