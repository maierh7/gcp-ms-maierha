#! /usr/bin/env python3

import sys
from oauth2client.client import GoogleCredentials as client

import opt
from lib.sqladm import SQLAdm

opt.parser.add_option ("", "--pid",  dest="pid", default=False, action="store_true")
opt.parser.add_option ("", "--proj", dest="proj")
opt.parser.add_option ("", "--inst", dest="inst")
opt.parser.add_option ("", "--back", dest="back", default=False, action="store_true")
opt.parser.add_option ("", "--del",  dest="delete", type=int)
opt.parser.add_option ("", "--old",  dest="old",  default=False, action="store_true")
opt.parser.add_option ("", "--exp",  dest="exp",  default=False, action="store_true")
opt.parser.add_option ("", "--all",  dest="all",  default=False, action="store_true")
opt.parser.add_option ("", "--full", dest="full", default=False, action="store_true")
opt.parser.add_option ("", "--last", dest="last", default=False, action="store_true")
opt.parser.add_option ("", "--rest", dest="rest" ) # backupID

opt.parser.add_option ("", "--trg_proj",  dest="trg_proj") # only new instance
opt.parser.add_option ("", "--trg_inst",  dest="trg_inst") # restore dialog


(opts, args) = opt.GetOptions ()

if opts.proj is None and opts.inst is None:
    print ("Error: missing arguments", file=sys.stderr)
    sys.exit (1)

cred = client.get_application_default()

sql = SQLAdm (opts.proj, opts.inst, cred)

if opts.back == True:
    sql.do_backup()
elif opts.delete is not None:
    print ("delete:", opts.delete)
    sql.delete_backup (opts.delete)
elif opts.pid == True:
    sql.print_bids ()
elif opts.old == True:
    sql.delete_old_backups ()
elif opts.exp == True:
    sql.export ()
elif opts.all:
    sql.get_backups_all (opts.full)
elif opts.trg_proj and opts.trg_inst:
    sql.get_backups (True)

    dct = dict ()
    
    ind = 0
    for i in sql.backups:
        et = sql.backups [i] [2]
        st = sql.backups [i] [3]
        if st != "SUCCESSFUL":
            continue
        dct [ind] = i
        print ("(%2d) %d %s %s" % (ind, int(i), et, st))
        ind += 1
    inp = input ("Index-Number: ")
    bid = dct[int (inp)]
    sql.restore_backup(bid, opts.trg_proj, opts.trg_inst)

elif opts.trg_proj:
    sql.create_instance (opts.trg_proj)
elif opts.rest is not None or opts.last == True:
    do_restore = input("Do you really want to restore the database (N/Y)?")
    if do_restore == 'Y':
        if opts.last == True:
            sql.restore_backup ()
        if opts.rest is not None:
            sql.restore_backup (opts.rest)
else:
    sql.print_version ()
    sql.print_backups (opts.full)
    sql.print_blst ()
    sql.print_bids ()

