#! /usr/bin/env python3

import re
import opt

opt.parser.add_option ("", "--pprint", default=False, action="store_true", dest="pprint")
opt.parser.add_option ("", "--proj", dest="proj")
opt.parser.add_option ("", "--parent", dest="parent")
opt.parser.add_option ("", "--folders", default=False, action="store_true", dest="folders")
opt.parser.add_option ("", "--product", default=False, action="store_true", dest="product")

(opts, args) = opt.GetOptions ()

from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

req = service.projects().list()

fld = set ()
pro = dict ()

while req:
    res = req.execute()
    for project in res.get('projects', []):
        # TODO: Change code below to process each `project` resource:

        if opts.parent is not None:
            if opts.parent != project['parent']['id']:
                continue
            
        fld.add (project['parent']['id'])
        if opts.product is True:
            if "labels" in project:
                if "product" in project['labels']:
                    m = re.search ("V135-(.*)", project['name'])
                    if m:
                        pro [m.group(1)] = [project ['projectId'], project ['name']]
        elif opts.proj is None or opts.proj == project['projectId']:
            print (project ['projectId'], project ['name'])
            if opts.pprint:
                pprint (project)
        req = service.projects().list_next(previous_request=req, previous_response=res)

if opts.folders is True:
    for i in fld:
        print (i)

if opts.product is True:
    for i in sorted (pro):
        print (pro[i][0], pro[i][1])
