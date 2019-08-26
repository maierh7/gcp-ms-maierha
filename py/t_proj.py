#! /usr/bin/env python3

from oauth2client.client import GoogleCredentials as client

import pro

cred = client.get_application_default()
proj = pro.Project (cred)
print (proj.get_id ("V135-5256-Playground-HaraldMai"))

