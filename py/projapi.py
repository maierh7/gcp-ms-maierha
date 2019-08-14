#! /usr/bin/env python3

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
        print (project ['name'])
    req = service.projects().list_next(previous_request=req, previous_response=res)

