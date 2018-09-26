#! /usr/bin/env python3

import opt
import sub

opt.parser.add_option ("-l", "--list", default=False, action="store_true", dest="list")
opt.parser.add_option ("-c", "--cur",  default=False, action="store_true", dest="cur")
opt.parser.add_option ("-a", "--acc",  default=False, action="store_true", dest="acc")

(opts, argv) = opt.GetOptions ()
        
if opts.list:
    sub.out_cmd ("gcloud projects list")

if opts.cur:
    sub.out_cmd ("gcloud config get-value project")    

if opts.acc:
    sub.out_cmd ("gcloud config get-value account")
