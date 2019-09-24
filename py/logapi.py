#! /usr/bin/env python3

import sys
import re
from datetime import datetime
from datetime import date
from datetime import timedelta

from google.cloud import logging

import opt

opt.parser.add_option ("", "--log",  dest="log")

(opts, args) = opt.GetOptions ()

logs = {
    "cf" : "projects/v135-5256-playground-haraldmai/logs/cloudfunctions.googleapis.com%2Fcloud-functions",
    "xb" : "projects/xbbcvpbxkziv/logs/cronjob-playground-mai-extented-backup-test-dev-euro"
    }

logres = {
    "cf" : ["resource.labels.function_name", "test-cf-ps-1"],
    "xb" : ["resource.labels.container_name", "cronjob-playground-mai-extented-backup-test-dev-euro"]
    }

import warnings
warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")

def trunc_sysdate ():
    dt = datetime.now ()
    dt = dt - timedelta (hours=3)
    dt = dt.replace (microsecond=0)
    return dt.isoformat () + "Z"

proj = None
glog = None

if opts.log is None:
    pass

log = logs[opts.log]
arr = re.split ("/", log)
proj = arr[1]
glog = arr[3]
    
print (proj, glog)

client = logging.Client ()

logger = client.logger (glog)

attr = logres[opts.log][0]
obj  = logres[opts.log][1]

filter = """\
{}="{}" AND timestamp >="{}"
""".format (attr, obj, trunc_sysdate ())

print (filter)

for i in list (logger.list_entries (projects=[proj], filter_=filter)):
    ts = i.timestamp.isoformat()
    pl = i.payload.strip ("\n")
    print (ts, pl)

