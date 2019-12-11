#! /usr/bin/env python3

import re
import os
import sys
import time

from pprint import pprint

from oauth2client.client import GoogleCredentials as client    
from googleapiclient import discovery
from googleapiclient.errors import HttpError

import fmt
from lib.sql    import SQL
from lib.sql    import SQL_Status
from lib.sql    import get_cpu_ram
from lib.pro    import Project
from lib.sqladm import SQLAdm

import lib.dp_pro as dp_pro
import lib.opt    as opt

opt.parser.add_option ("", "--crit",   default=False, action="store_true", dest="crit")
opt.parser.add_option ("", "--v135",   default=False, action="store_true", dest="v135")
opt.parser.add_option ("", "--size",   default=False, action="store_true", dest="size")
opt.parser.add_option ("", "--dr",     default=False, action="store_true", dest="dr")
opt.parser.add_option ("", "--full",   default=False, action="store_true", dest="full")
opt.parser.add_option ("", "--sa",     default=False, action="store_true", dest="sa")
opt.parser.add_option ("", "--all",    default=False, action="store_true", dest="all")
opt.parser.add_option ("", "--status", default=False, action="store_true", dest="status")
opt.parser.add_option ("", "--tier",   default=False, action="store_true", dest="tier")
opt.parser.add_option ("", "--alltier",default=False, action="store_true", dest="alltier")
opt.parser.add_option ("", "--back",   default=False, action="store_true", dest="back")

opt.parser.add_option ("", "--pro",    dest="pro")

(opts, args) = opt.GetOptions ()

excl = (
#    "nf1bkafm142j",
    "mms-bdg-privsql-a-sqlp",
    "mms-cfo-wtf-p",
    )

crit = {
    "search-prod" : "urotlgsjtbfy",
    "teasermanagement-prod" : "lya18fxlcdd3",
    "price-calc-prod" : "efbtokmry9d8",
    "product-data-prod" : "hcflusagqbjm",
    "catalog-data-api-prod" : "h3fkajhwg6dl",
    "subscriptions-prod" : "b3ykg4yec56b",
    "olm-prod" : "phkrn1bc9yag",
    "order-change-ex-prod" : "ttypvc4xdebh",
    "dmc-prod" : "duuni0vc7ohq",
    "xpay-prod" : "q81ue9gsrzxv",
    "fraud-prod" : "mluqtkbhifci",
    }
    
sqlp = {
    "V135-5256-Playground-HaraldMai" : "v135-5256-playground-haraldmai",
    # "V135-playground-mai-dev" :        "xbbcvpbxkziv",
    # "6117V135-myaccount-prod" :        "aq12fq1g0adk",
    # "6117V135-myaccount-dev"  :        "u1f3rwmxbxdt",
    }

cred = client.get_application_default()

def get_v135_p ():
    pro = dict ()
    dir = os.environ ['HOME'] + "/cfo/git/gcp-ms-maierha/doc/"
    fp = open (dir + "proj-v135.txt")
    for i in fp:
        i = i.strip ("\n")
        res = re.split (" ", i)
        if len (res) == 2:
            id = re.sub ("^[0-9]+V[0-9]+-", "", res[1])
            pro [id] = res[0]
        
    fp.close ()
    return pro

def get_projects ():
    pro = dict ()
    if opts.crit is True:
        return crit
    elif opts.v135 is True:
        return get_v135_p ()
    else:
        for i in dp_pro.plist:
            if opts.pro is not None:
                if dp_pro.plist [i] == opts.pro:
                    pro [i] = dp_pro.plist [i]
            else:
                pro [i] = dp_pro.plist [i]
    return pro
    
if opts.full is True:
    for i in sqlp:
        sql = SQL (sqlp[i], cred)
        pprint (sql.items)
elif opts.alltier is True:
    sql = SQL (sqlp ["V135-5256-Playground-HaraldMai"], cred)
    sql.get_all_tiers ()
elif opts.size is True:

    fmt.heading ({
        "Size"   : 4,
        "H-Type" : 6,
        "BC"     : 2,
        "D-Type" : 12,
        "Name"   : 25,
        })
    
    pro = sqlp
    if opts.all == True:
        pro = get_projects ()

    for i in sorted (pro):
        sql = SQL (pro[i], cred)
        res = sql.get_size ()
        for j in res:
            cnt = 0
            if pro[i] not in excl:
                cnt = sql.get_backup_count (j)
            print ("%4s %s %2d %12s %25s %s %s" %
                       (res[j][1], res[j][2], cnt, res[j][0], j, pro[i], i))
    
elif opts.dr is True:
    pro = sqlp
    if opts.all == True:
        pro = get_projects ()

    for i in sorted (pro):
        sql = SQL (pro[i], cred)
        res = sql.get_dr ()
        for j in res:
            print ("%8s %5s %5s %25s  %s %s" %
                       (res[j][0], res[j][1], res[j][2],j, pro[i], i))
        
elif opts.sa is True:
    pro = sqlp
    if opts.all == True:
        pro = get_projects ()

    for i in pro:
        sql = SQL (sqlp[i], cred)
        sa = sql.get_sa ()

        for i in sa:
            print (i, sa[i])

elif opts.status is True:
    pro = sqlp
    if opts.all is True:
        pro = get_projects ()

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

elif opts.tier is True:
    pro = sqlp
    if opts.all is True:
        pro = get_projects ()
    for i in sorted (pro):
        sql = SQL (pro[i], cred)

        for j in sql.items:
            res = get_cpu_ram (j['settings']['tier'])
            print ("%3d %5.2f %20s %s" % (res[0], res[1],j['name'], i))

elif opts.back is True:
    pro = sqlp
    if opts.all is True:
        pro = get_projects ()
    for i in sorted (pro):
        sql = SQL (pro[i], cred)

        for j in sql.items:
            if "settings" in j:
                if "backupConfiguration" in j['settings']:
                    if j['settings']['backupConfiguration']['enabled'] is False:
                        print (pro[i], i, j['name'])
else:

    pro = sqlp
    if opts.all == True:
        pro = get_projects ()

    for i in pro:
        sql  = SQL (pro[i], cred)
        inst = sql.list ()
    
        for j in inst:
            print ("--proj %s --inst %s" % (pro[i], j))
