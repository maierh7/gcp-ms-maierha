#! /usr/bin/env python3


import sys
import json

import opt

opt.parser.add_option ("", "--sec", dest="sec", default="all")

(opts, args) = opt.GetOptions ()

secs = (
"hm-uname:",       
"hm-env:",
"hm-apk:",
"hm-ls-usr:",
"hm-ls-usr-local:",
"hm-type:",
    )
 
if len (args) == 0:
    print ("Error: no log file")
    sys.exit (1)
 
prt = False
with open (args[0]) as f:
    data = json.load (f)
    data.reverse ()
    for i in data:
        out = i["textPayload"]
        out  = out.strip ("\n")
        if opts.sec == "all":
            print (out)
        else:
            if out == opts.sec:
                prt = True
            elif out in secs:
                prt = False
            if prt == True:
                print (out)
