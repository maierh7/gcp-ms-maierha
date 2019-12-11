#! /usr/bin/env python3

import opt

from pprint import pprint
from oauth2client.client import GoogleCredentials as client
from googleapiclient import discovery

opt.parser.add_option ("", "--proj", dest="proj", default="v135-5256-playground-haraldmai")

(opts, args) = opt.GetOptions ()

cred = client.get_application_default ()

iam = discovery.build ("iam", "v1", credentials=cred)

body = {
    "fullResourceName" : "//cloudresourcemanager.googleapis.com/projects/" + opts.proj
    }

while True:
    req = iam.permissions().queryTestablePermissions (body=body)
    res = req.execute ()

    for i in res.get ('permissions', []):
        api = True
        if 'apiDisabled' in i:
            api = False
        nam = i['name']
        sta = i['stage']
        print ("%5s %5s %s" % (api, sta, nam))
        
    if 'nextPageToken' not in res:
        break
    #body ['fullResourceName'] = body ['fullResourceName']
    body ['pageToken'] = res['nextPageToken']
