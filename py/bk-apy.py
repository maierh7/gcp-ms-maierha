#! /usr/bin/env python3


import sys
import pprint

import json
from apiclient import discovery
from oauth2client.client import GoogleCredentials as client

import opt

opt.parser.add_option ("", "--pro", type="int", default=0, dest="proj")
opt.parser.add_option ("", "--ins", action="store_true", default=False, dest="ins")
opt.parser.add_option ("", "--del", action="store_true", default=False, dest="delete")

(opts, args) = opt.GetOptions ()


proj = (
    "xbbcvpbxkziv",
    "v135-5256-playground-haraldmai",
    )

bcks = dict ()

cred = client.get_application_default()
sql  = discovery.build ("sqladmin", "v1beta4",credentials=cred)

res = sql.instances ().list(project=proj[opts.proj]).execute ()

for i in res['items']:
    for j in i:
        if j in ("serverCaCert", "settings", "etag"):
            continue
        print (j, i[j])

if opts.ins == True:
    body = {}
    res = sql.backupRuns ().insert (project=proj[0], instance="dev-europe-west4-b", body=body).execute ()
    pprint.pprint (res)

if opts.delete == True:
    res = sql.backupRuns ().list (project=proj[0], instance="dev-europe-west4-b").execute ()
    for i in res['items']:
        bid = None
        for j in i:
            if j == "id":
                bid = i[j]
                bcks [bid] = list ()
                print (j, bid)
            if j == "endTime":
                bcks [bid].append (i[j])
    for i in bcks:
        print (i, bcks[i])
        res = sql.backupRuns ().delete (project=proj[0], instance="dev-europe-west4-b", id=i).execute ()
                
