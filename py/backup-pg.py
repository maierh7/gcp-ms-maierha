#! /usr/bin/env python3

import sys
import opt
import sqladm

from oauth2client.client import GoogleCredentials as client

opt.parser.add_option ("", "--proj",  dest="proj")
opt.parser.add_option ("", "--inst",  dest="inst")
opt.parser.add_option ("", "--print", dest="print", default=True, action="store_true")

(opts, args) = opt.GetOptions ()

if opts.proj is None and opts.inst is None:
    print ("Error: missing arguments", file=sys.stderr)
    sys.exit (1)

cred = client.get_application_default()

sql = sqladm.SQLAdm (opts.proj, opts.inst, cred)

if opts.print:
    sql.print_version ()
    sql.print_blst ()
else:
    sql.do_backup ()
