#! /usr/bin/env python3

import sub
import opt

opt.parser.add_option ("", "--tsql", default=False, action="store_true", dest="tsql")

(opts, args) = opt.GetOptions ()

lst = {
"V135-5256-Playground-HaraldMai" : ["v135-5256-playground-haraldmai", "hm1-pg"],
"V135-playground-mai-dev"        : ["xbbcvpbxkziv", "dev-europe-west4-b"],
"6117V135-myaccount-prod"        : ["aq12fq1g0adk", "prod-europe-west4-b"],
"6117V135-myaccount-dev"         : ["u1f3rwmxbxdt", "dev-europe-west4-b"],
    }


def list_backup (entry):
    proj = entry[0]
    inst = entry[1]
    print (proj, inst)
    prog="backup-pg.py"
    if opts.tsql == True:
        prog="t_sqladm.py"
    cmd = prog + " --proj " + proj + " --inst " + inst
    if opts.tsql != True:
        cmd += " --list"
    sub.out_cmd (cmd)

idx = 0
for i in lst:
    print ("%3d %s" % (idx, i))
    idx += 1
inp = int(input ("Get number :"))
# print (inp)
# print (lst[list (lst.keys ()) [inp]])
list_backup ((lst[list (lst.keys ()) [inp]]))

