#! /usr/bin/env python3

import sys
from oauth2client.client import GoogleCredentials as client

import opt
import sqladm

opt.parser.add_option ("", "--proj", dest="proj")
opt.parser.add_option ("", "--inst", dest="inst")
opt.parser.add_option ("", "--back", dest="back", default=False, action="store_true")
opt.parser.add_option ("", "--del24", dest="del24", default = False, action="store_true")
opt.parser.add_option ("", "--del",  dest="delete", type=int)

(opts, args) = opt.GetOptions ()

if opts.proj is None and opts.inst is None:
    print ("Error: missing arguments", file=sys.stderr)
    sys.exit (1)

cred = client.get_application_default()

sql = sqladm.SQLAdm (opts.proj, opts.inst, cred)

if opts.back == True:
    sql.do_backup()
elif opts.delete is not None:
    print ("delete:", opts.delete)
    sql.delete_backup (opts.delete)
elif opts.del24 == True:
    sql.delete_backup_less_24 ()
else:
    sql.print_version ()
    sql.print_backups ()
    sql.print_blst ()
    sql.print_bids ()

