#! /usr/bin/env python3

import opt

opt.parser.add_option ("", "--pprint", default=False, action="store_true", dest="pprint")
opt.parser.add_option ("", "--proj", dest="proj")

(opts, args) = opt.GetOptions ()

from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

req = service.projects().list()

while req:
    res = req.execute()
    for project in res.get('projects', []):
        # TODO: Change code below to process each `project` resource:

        if opts.proj is None or opts.proj == project['projectId']:
            print (project ['projectId'], project ['name'])
            if opts.pprint:
                pprint (project)
        req = service.projects().list_next(previous_request=req, previous_response=res)

