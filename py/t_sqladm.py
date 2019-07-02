#! /usr/bin/env python3

import sys
from oauth2client.client import GoogleCredentials as client

import opt
import sqladm

opt.parser.add_option ("", "--proj", dest="proj")
opt.parser.add_option ("", "--inst", dest="inst")

(opts, args) = opt.GetOptions ()

if opts.proj is None and opts.inst is None:
    print ("Error: missing arguments", file=sys.stderr)
    sys.exit (1)

cred = client.get_application_default()

sql = sqladm.SQLAdm (opts.proj, opts.inst, cred)
sql.get_backups ()
sql.print_backups ()
sql.print_blst ()
sql.print_bids ()
