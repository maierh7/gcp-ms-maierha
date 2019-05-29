#! /usr/bin/env python3

import opt
import sub

# sql.py --list
# sql.py --list --back -inst <inst>

opt.parser.add_option ("", "--list", default=False, action="store_true", dest="list")
opt.parser.add_option ("", "--back", default=False, action="store_true", dest="back")
opt.parser.add_option ("", "--inst", dest="inst")

(opts, args) = opt.GetOptions ()

if opts.back == True and opts.list == True and opts.inst:
    sub.out_cmd ("gcloud sql backups list -i " + opts.inst)
elif opts.list:
    sub.out_cmd ("gcloud sql instances list")

