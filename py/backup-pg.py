#! /usr/bin/env python3

import re
import opt
import sys
import subprocess
from datetime import date
from datetime import time
from datetime import timedelta
from datetime import datetime

import utc

opt.parser.add_option ("", "--inst", dest="inst")
opt.parser.add_option ("", "--list", default=False, action="store_true", dest="list")
opt.parser.add_option ("", "--keep", type="int", default=14, dest="keep")

(opts, args) = opt.GetOptions ()

nd = utc.UTC ()
na = nd.date ()

# blst [<date>] (<datetimes>, ...)
blst = dict ()
# bids [<datetime>] = <Backup ID>
bids = dict ()
    
def get_backups ():
    blst.clear ()
    out = subprocess.check_output ("gcloud sql backups list --instance " + opts.inst, shell = True).decode ("utf-8")
    lines = out.splitlines ()
    for i in lines:
        res = re.split (" +", i)
        dtr = re.match ("[0-9-]+T[0-9:.+]+", res[1])
        if len(res) > 0 and dtr:
            #print (res[1])
            id = res[0]
            dt = datetime.strptime (res[1], "%Y-%m-%dT%H:%M:%S.%f%z")
            da = dt.date ()
            #print (da, ti)
            if da not in blst:
                blst[da] = list ()
            blst [da].append (dt)
            bids [dt] = id

def print_blst ():
    print ("Now:")
    print (str (na) + ":", nd.time ())
    print ("Backup-List")
    for i in sorted (blst, reverse=True):
        print (i, end=": ")
        for j in blst[i]:
            print (j.replace(microsecond=0).time (), end=" ")
        print ()

def do_backup ():
    backup = False
    if na not in blst:
        backup = True
    else:
        cur_last = blst[na][0]
        print (nd.utc, cur_last + timedelta (minutes=60))
        if nd.utc > cur_last + timedelta (minutes=60):
            backup = True
    print (backup)
    
    if backup == True:
        res = subprocess.run ("gcloud sql backups create --instance=" + opts.inst, shell=True)
        if res.returncode != 0:
            sys.exit (1)
        else:
            get_backups ()

def print_bids ():
    print ("IDs:")
    for i in sorted (bids, reverse=True):
        print (bids[i], i)
            
if opts.inst is None:
    print ("Error: no instance", file=sys.stderr)
    sys.exit (1)

if opts.list == True:
    get_backups ()
    print_blst ()
    sys.exit ()

get_backups ()
do_backup ()
print_blst ()
print_bids ()
