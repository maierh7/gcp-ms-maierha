#! /usr/bin/env python3

import time

from oauth2client.client import GoogleCredentials as client    
from googleapiclient import discovery
from googleapiclient.errors import HttpError

from lib.sql    import SQL
from lib.sql    import SQL_Status
from lib.pro    import Project
from lib.sqladm import SQLAdm

import lib.opt as opt

opt.parser.add_option ("", "--sa",  default=False, action="store_true", dest="sa")
opt.parser.add_option ("", "--all", default=False, action="store_true", dest="all")
opt.parser.add_option ("", "--pro", dest="pro")

(opts, args) = opt.GetOptions ()

excl = (
    # "vvvcxwdwj1xa",
    # "sys-48609460970177310285461281"
    )
 
sqlp = {
    "V135-5256-Playground-HaraldMai" : "v135-5256-playground-haraldmai",
    "V135-playground-mai-dev" :        "xbbcvpbxkziv",
    "6117V135-myaccount-prod" :        "aq12fq1g0adk",
    "6117V135-myaccount-dev"  :        "u1f3rwmxbxdt",
    }

cred = client.get_application_default()

if opts.all:
    res = dict ()
    res [SQL_Status.LIST]  = 0
    res [SQL_Status.EMPTY] = 0
    res [SQL_Status.PERM]  = 0
    
    pro  = Project (cred)
    print ("Project-Count", len (pro.plst))
    for i in pro.plst:
        if opts.pro is not None:
            if opts.pro != pro.plst[i]:
                continue
        pid = pro.plst[i]

        if pid in excl:
            continue
        sql = SQL (pid, cred)
        res [sql.status] += 1
        if sql.status == SQL_Status.LIST:
            lst = sql.list ()
            print ("%1d %30s %s" % (len (lst), pid, i))
            for j in lst:
                cnt = sql.get_backup_count (j, cred)
                print ("  %2d %s" % (cnt, j))

    print ("Project-Count", len (pro.plst))
    for i in res:
        print (i, res[i])
            
elif opts.sa:
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
