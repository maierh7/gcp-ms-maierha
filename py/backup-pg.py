#! /usr/bin/env python3

import sys
import opt
import sqladm

from oauth2client.client import GoogleCredentials as client

opt.parser.add_option ("", "--proj",   dest="proj")
opt.parser.add_option ("", "--inst",   dest="inst")
opt.parser.add_option ("", "--delete", dest="delete", default=False, action="store_true")
opt.parser.add_option ("", "--list",   dest="list",  default=False, action="store_true")

(opts, args) = opt.GetOptions ()

if opts.proj is None and opts.inst is None:
    print ("Error: missing arguments", file=sys.stderr)
    sys.exit (1)

cred = client.get_application_default()

sql = sqladm.SQLAdm (opts.proj, opts.inst, cred)

if opts.list:
    sql.print_version ()
    sql.print_blst ()
elif opts.delete:
    sql.delete_old_backups ()
else:
    sql.delete_old_backups ()
    sql.do_backup ()
