#! /usr/bin/env python3

from oauth2client.client import GoogleCredentials as client    
from googleapiclient import discovery
from googleapiclient.errors import HttpError

from lib.sql import SQL

import lib.opt as opt

opt.parser.add_option ("", "--sa", default=False, action="store_true", dest="sa")

(opts, args) = opt.GetOptions ()

sqlp = {
    "V135-5256-Playground-HaraldMai" : "v135-5256-playground-haraldmai",
    "V135-playground-mai-dev" :        "xbbcvpbxkziv",
    "6117V135-myaccount-prod" :        "aq12fq1g0adk",
    "6117V135-myaccount-dev"  :        "u1f3rwmxbxdt",
    }

cred = client.get_application_default()

if opts.sa:
    for i in sqlp:
        sql = SQL (sqlp[i], cred)
        sa = sql.get_sa ()

        for i in sa:
            print (i, sa[i])
else:

    for i in sqlp:
        sql  = SQL (sqlp[i], cred)
        inst = sql.list ()
    
        for j in inst:
            print ("--proj %s --inst %s" % (sqlp[i], j))
