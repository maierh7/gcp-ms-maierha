#! /usr/bin/env python3

import re
import os
from pro import Project
from oauth2client.client import GoogleCredentials



home = os.environ ['HOME']
dp_dir = home + "/cfo/git/terraform-google-digital-platform/config"

cred = GoogleCredentials.get_application_default()

pro = Project (cred)

def get_pro (dp):
    for i in pro.plst:
        m = re.search (dp, i)
        if m:
            return pro.plst[i]

for i in os.listdir (dp_dir):
    i = re.sub("\.tfvars$", "", i)
    pid = get_pro (i)
    print (pid, i)
