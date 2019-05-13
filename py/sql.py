#! /usr/bin/env python3

import opt
import sub

opt.parser.add_option ("", "--list", default=False, action="store_true", dest="list")

(opts, args) = opt.GetOptions ()

if opts.list:
    sub.out_cmd ("gcloud sql instances list")


