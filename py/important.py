#! /usr/bin/env python3

import os
import sys
import subprocess as sub

from pro import Project

from pathlib import Path

from pprint import pprint
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials as client
from googleapiclient import discovery

file = os.environ ["HOME"] + "/cfo/git/gcp-ms-maierha/doc/proj-v135.txt"

path = Path (file)

if path.exists () is False:
    print ("Error: file does not exists", file = sys.stderr)
    sys.exit ()

lst = (
    "tc0cbnlbf379",
    "urotlgsjtbfy",
    "zrbw4naek7lw",
    "lya18fxlcdd3",
    "cxc9srvfqci1",
    "xmlgazteinet",
    "ospdbcvsabjp",
    "jmrzcodxl7dy",
    "uazvwrccscc1",
    "mms-gib-promotion-p-1337",
    "efbtokmry9d8",
    "eqp99ndhwoag",
    "t1d9ucfyu5jc",
    "hcflusagqbjm",
    "h3fkajhwg6dl",
    "b3ykg4yec56b",
    "phkrn1bc9yag",
    "ttypvc4xdebh",
    "duuni0vc7ohq",
    "espeyu24idev",
    "q81ue9gsrzxv",
    "mluqtkbhifci",
    )

cred = client.get_application_default ()
pro = Project (cred)
sql = discovery.build ("sqladmin", "v1beta4", credentials=cred)
    
# for i in lst:
#     sub.run ("grep " + i + " " + file, shell=True) 

for i in lst:
    na = pro.get_name (i)
    if na is None:
        print ("Error: not a project id (" + i + ")")
        continue
    req = sql.instances().list (project=i)
    try:
        res = req.execute ()
    except HttpError as err:
        if err.resp.status == 403:
            print ("%25s %25s %s" % (i, "no access", na))
            continue

    if len (res) == 0:
        print ("%25s %25s %s" % (i, "no instance", na))
    else:
        for j in res ['items']:
            print ("%25s %25s %s" % (i, j['name'], na))

