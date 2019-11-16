#! /usr/bin/env python3

import re
import os
import time

from pprint import pprint

from oauth2client.client import GoogleCredentials as client    
from googleapiclient import discovery
from googleapiclient.errors import HttpError

import fmt
from lib.sql    import SQL
from lib.sql    import SQL_Status
from lib.pro    import Project
from lib.sqladm import SQLAdm

import lib.opt as opt

opt.parser.add_option ("", "--size",   default=False, action="store_true", dest="size")
opt.parser.add_option ("", "--dr",     default=False, action="store_true", dest="dr")
opt.parser.add_option ("", "--full",   default=False, action="store_true", dest="full")
opt.parser.add_option ("", "--sa",     default=False, action="store_true", dest="sa")
opt.parser.add_option ("", "--all",    default=False, action="store_true", dest="all")
opt.parser.add_option ("", "--status", default=False, action="store_true", dest="status")

(opts, args) = opt.GetOptions ()

excl = (
    "nf1bkafm142j"
    )
 
sqlp = {
    "V135-5256-Playground-HaraldMai" : "v135-5256-playground-haraldmai",
    "V135-playground-mai-dev" :        "xbbcvpbxkziv",
    "6117V135-myaccount-prod" :        "aq12fq1g0adk",
    "6117V135-myaccount-dev"  :        "u1f3rwmxbxdt",
    }

cred = client.get_application_default()

def get_projects (pro):
    pro.clear ()
    fp = open (os.environ['HOME'] + "/tmp/dp-pro.lis")
    for i in fp:
        i = i.strip ("\n")
        arr = re.split (" ", i)
        pro[arr[1]] = arr[0]
    fp.close ()

if opts.full:
    for i in sqlp:
        sql = SQL (sqlp[i], cred)
        pprint (sql.items)

elif opts.size:

    fmt.heading ({
        "Size"   : 4,
        "H-Type" : 6,
        "BC"     : 2,
        "D-Type" : 12,
        "Name"   : 25,
        })
    
    pro = sqlp
    if opts.all == True:
        get_projects (pro)

    for i in sorted (pro):
        sql = SQL (pro[i], cred)
        res = sql.get_size ()
        for j in res:
            cnt = 0
            if pro[i] not in excl:
                cnt = sql.get_backup_count (j)
            print ("%4s %s %2d %12s %25s %s %s" %
                       (res[j][1], res[j][2], cnt, res[j][0], j, pro[i], i))
    
elif opts.dr:
    pro = sqlp
    if opts.all == True:
        get_projects (pro)

    for i in sorted (pro):
        sql = SQL (pro[i], cred)
        res = sql.get_dr ()
        for j in res:
            print ("%8s %5s %5s %25s  %s %s" %
                       (res[j][0], res[j][1], res[j][2],j, pro[i], i))
        
elif opts.sa:
    pro = sqlp
    if opts.all == True:
        get_projects (pro)

    for i in pro:
        sql = SQL (sqlp[i], cred)
        sa = sql.get_sa ()

        for i in sa:
            print (i, sa[i])

elif opts.status:
    pro = sqlp
    if opts.all is True:
        get_projects (pro)

    res = {
        SQL_Status.EMPTY : 0,
        SQL_Status.LIST  : 0,
        SQL_Status.PERM  : 0,
        }

    for i in sorted (pro):
        sql = SQL (pro[i], cred)
        sta = re.sub ("SQL_Status.", "", str (sql.status))
        res [sql.status] += 1
        print ("%5s %s %s" % (sta, pro[i], i))

    for i in res:
        print ("%2d %s" % (res[i], i))

else:

    for i in sqlp:
        sql  = SQL (sqlp[i], cred)
        inst = sql.list ()
    
        for j in inst:
            print ("--proj %s --inst %s" % (sqlp[i], j))
