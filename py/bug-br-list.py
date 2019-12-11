#! /usr/bin/env python3

import sys
import string
import random
import time

from pprint   import pprint
from optparse import OptionParser

from oauth2client.client import GoogleCredentials as client
from googleapiclient import discovery

def get_rand_postfix ():
    postfix = ''.join (random.choice(string.ascii_lowercase) for _ in range (4))
    return postfix

parser = OptionParser()
parser.add_option ("", "--project", dest="project")
parser.add_option ("", "--backend", dest="backend", default="SECOND_GEN")
parser.add_option ("", "--version", dest="version", default="POSTGRES_9_6")

(opts, args) = parser. parse_args ()
 
if opts.project is None:
    print ("Error: --project missing", file = sys.stderr)
    
cred = client.get_application_default ()

sql = discovery.build ("sqladmin", "v1beta4", credentials=cred)

body = {
    "name" : "test-" + get_rand_postfix (),
    "backendType"     : opts.backend,
    "databaseVersion" : opts.version,
    "settings" : {
        "tier" : "db-f1-micro",
        }
    }

pprint (body)
req = sql.instances().insert (project=opts.project, body=body)
res = req.execute ()

print (body["name"])

while True:
    req = sql.instances().get (project=opts.project, instance=body ["name"])
    res = req.execute ()
    print (res["state"])
    if res['state'] == "RUNNABLE":
        break
    time.sleep (60)

req = sql.backupRuns ().list (project=opts.project, instance=body["name"])
while req:
    res = req.execute ()
    req = sql.backupRuns().list_next (previous_request=req, previous_response=res)

